import json
import sys

def change_in_open_interest(
    # spot, strikes, expiry_list, expiry, index, container_window
    # spot, strikes, expiry_list, expiry, index, container_window
    content,
    index
):
    global atm

    spot_ = float(content["records"]["underlyingValue"])
    strikes = content["records"]["strikePrices"]
    expiry_list = content["records"]["expiryDates"]

    index_dict = {
        "NIFTY": {"slicer": 25, "lot_size": 50},
        "BANKNIFTY": {"slicer": 100, "lot_size": 25},
        "USDINR": {
            "slicer": 0.1250,
            "lot_size": 1,
        },  #  USDINR is leveraged for 1000 USD for 1 Qty
    }

    atm_slicer = index_dict[index]["slicer"]
    lot_size = index_dict[index]["lot_size"]

    f_strikes = []
    call_oi = []
    put_oi = []
    call_change_oi = []
    put_change_oi = []


    for item in content["records"]["data"]:

        if item["strikePrice"] in strikes:

            if item["expiryDate"] == expiry:

                # check for strikes
                f_strikes.append(item["strikePrice"])

                # Check and add Call OI, Call OI change
                if "CE" in item.keys():
                    call_oi.append(item["CE"]["openInterest"])
                    call_change_oi.append(item["CE"]["changeinOpenInterest"])
                else:
                    call_oi.append(0)
                    call_change_oi.append(0)

                # Check and add Put OI
                if "PE" in item.keys():
                    put_oi.append(item["PE"]["openInterest"])
                    put_change_oi.append(item["PE"]["changeinOpenInterest"])
                else:
                    put_oi.append(0)
                    put_change_oi.append(0)

            else:
                pass

        else:
            print("fail")

    atm_oi_yval = max(max(call_oi), max(put_oi))
    atm_change_oi_yval = max(max(call_change_oi), max(put_change_oi))

    # Contract values calculation in million
    calls = round(lot_size * sum(call_oi) / 1000000, 2)
    puts = round(lot_size * sum(put_oi) / 1000000, 2)
    calls_change = round(lot_size * sum(call_change_oi) / 1000000, 2)
    puts_change = round(lot_size * sum(put_change_oi) / 1000000, 2)
    return puts_change,calls_change





if __name__ == '__main__':
    global start_time
    global end_time
    global selected_index 
    global expiry
    selected_time  = input("Select Index (NIFTY or BANKNIFTY) :- ")
    
    with open(f"{selected_time}-chain.json","r") as file:
        content = json.load(file)
    keys = list(content.keys())
    expiryDatesList =   content[keys[0]]["records"]["expiryDates"]
    for i,m in enumerate(expiryDatesList):
        print(f"{i+1}. {m}")
    expiry  = expiryDatesList[int(input("Enter a number for expiry Date from list above :- "))-1]
    print("List of data available for time")
    for i,m in enumerate(keys):
        print(f"{i+1}. {m}")
    start= int(input("Enter start time:- "))-1
    end  = int(input("Enter end time :- "))-1
    if(start > end):
        print("invalid time range")
        exit()
    start_time = keys[start]
    end_time = keys[end]
    

   
    (start_puts,start_calls) =  change_in_open_interest(content[start_time], selected_time)
    (end_puts,end_calls) = change_in_open_interest(content[end_time], selected_time)
    print(f"Put change:- {end_puts-start_puts}")
    print(f"Call change:- {end_calls-start_calls}")
    