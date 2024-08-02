import re
import logging
import serial
import time
from helper import Helper
import gparams
# Perform the regex search and extraction
def extract_values(pattern, response):
    match = re.search(pattern, response)
    if match:
        return match.groupdict()
    else:
        return None


class Modem:
    def __init__(self):
        self.connected = False
        self.ppp = None
        self.serial = None
        self.apn = None
        self.data_over_ppp = True

    def initialize_port(self, port, baud_rate, timeout):
        self.serial = serial.Serial(port, baud_rate, timeout=timeout)

    def send_at_command(self, command, timeout=0.5):
        try:
            # Open the serial port
            self.serial.write((command + '\r\n').encode())
            time.sleep(timeout + 0.1)
            # Read the response
            response = self.serial.read_all().decode()
            print(response)
            return response

        except Exception as e:
            return f"Error: {e}"

    def is_alive(self):
        status = self.send_at_command("AT", 0.5)
        return status

    def print_status(self):
        self.send_at_command("AT+CFUN?")
        self.send_at_command("AT+CMEE=2")
        self.send_at_command("AT+CPIN?")
        self.send_at_command("AT+QDSIM?")
        self.send_at_command("AT+QSIMVOL?")
        self.send_at_command("AT+QSIMDET?")

    def get_prefered_mode(self):
        response = self.send_at_command("AT+QNWPREFCFG=\"mode_pref\"")
        # Define the regular expression to match the mode preferences
        pattern = r'QNWPREFCFG: \"mode_pref\",(.*)'
        # Search for the pattern in the response
        match = re.search(pattern, response)
        if match:
            # Extract the modes from the matched group
            modes = match.group(1).split(':')
            return [mode.strip() for mode in modes]
        else:
            return []
        return mode_pref

    def set_prefered_mode(self, mode):
        response = self.send_at_command("AT+QNWPREFCFG=\"mode_pref\"," + mode)
        return response

    def get_oper_and_mode(self):
        response = self.send_at_command("AT+COPS?")
        pattern = r'\+COPS: \d+,\d+,"([^"]+)",(\d+)'

        # Search for the pattern in the response
        match = re.search(pattern, response)
        if match:
            operator = match.group(1)
            act = match.group(2)
            return operator, act
        else:
            return None, None

    def get_apn(self):
        response = self.send_at_command("AT+CGDCONT?")
        # Define the regular expression to match the CGDCONT response
        pattern = r'\+CGDCONT: (\d+),"([^"]+)","([^"]+)"'

        # Find all matches in the response
        matches = re.findall(pattern, response)
        # Dictionary to store the CID and corresponding APN
        cgdcont_info = {}
        for match in matches:
            cid = match[0]
            apn = match[2]
            cgdcont_info[cid] = apn
        return apn

    def set_apn(self, apn):
        response = self.send_at_command("AT+CGDCONT=1,\"IP\",\"" + apn + "\"")
        return response

    def get_csq(self):
        response = self.send_at_command("AT+CSQ")
        # Define the regular expression to match the CSQ response
        pattern = r'\+CSQ: (\d+),(\d+)'
        # Search for the pattern in the response
        match = re.search(pattern, response)

        if match:
            rssiX = match.group(1)
            if rssiX == 0:
                rssi = -113
            elif rssiX == 1:
                rssi = -111
            elif rssiX == 31:
                rssi = -51
            elif rssiX == 99:
                rssi = 99
            else:
                rssi = -109 + 2 * (float(rssiX) - 2)

            ber = float(match.group(2))
            if ber == 0:
                ber = 0.001
            elif ber == 1:
                ber = 0.003
            elif ber == 2:
                ber = 0.0064
            elif ber == 3:
                ber = 0.013
            elif ber == 4:
                ber = 0.027
            elif ber == 5:
                ber = 0.054
            elif ber == 6:
                ber = 0.11
            elif ber == 7:
                ber = 0.15
            elif ber == 99:
                ber = 99

            return rssi, ber
        else:
            return None, None

    def get_qrsrp(self):
        response = self.send_at_command("AT+QRSRP")
        # Define the regular expression to match the QRSRP response
        pattern = r'\+QRSRP: (-?\d+),(-?\d+),(-?\d+),(-?\d+),(\w+)'
        # Search for the pattern in the response
        match = re.search(pattern, response)
        if match:
            rsrp_prx = match.group(1)
            rsrp_drx = match.group(2)
            rsrp_rx2 = match.group(3)
            rsrp_rx3 = match.group(4)
            rsrp_sysmode = match.group(5)
            return rsrp_prx, rsrp_drx, rsrp_rx2, rsrp_rx3, rsrp_sysmode
        else:
            return None, None, None, None, None

    def get_qrsrq(self):
        response = self.send_at_command("AT+QRSRQ")
        # Define the regular expression to match the QRSRP response
        pattern = r'\+QRSRQ: (-?\d+),(-?\d+),(-?\d+),(-?\d+),(\w+)'
        # Search for the pattern in the response
        match = re.search(pattern, response)
        if match:
            rsrq_prx = match.group(1)
            rsrq_drx = match.group(2)
            rsrq_rx2 = match.group(3)
            rsrq_rx3 = match.group(4)
            rsrq_sysmode = match.group(5)
            return rsrq_prx, rsrq_drx, rsrq_rx2, rsrq_rx3, rsrq_sysmode
        else:
            return None, None, None, None, None

    def get_qsinr(self):
        response = self.send_at_command("AT+QSINR")
        # Define the regular expression to match the QRSRP response
        pattern = r'\+QSINR: (-?\d+),(-?\d+),(-?\d+),(-?\d+),(\w+)'
        # Search for the pattern in the response
        match = re.search(pattern, response)
        if match:
            sinr_prx = match.group(1)
            sinr_drx = match.group(2)
            sinr_rx2 = match.group(3)
            sinr_rx3 = match.group(4)
            sinr_sysmode = match.group(5)
            return sinr_prx, sinr_drx, sinr_rx2, sinr_rx3, sinr_sysmode
        else:
            return None, None, None, None, None

    def get_net_info(self):
        response = self.send_at_command("AT+QNWINFO")
        # Define the regular expression to match the QNWINFO response
        pattern = r'\+QNWINFO: "([^"]+)","([^"]+)","([^"]+)",(\d+)'
        # Find all matches in the response
        matches = re.findall(pattern, response)
        qnwinfo_info = []

        for match in matches:
            network_type = match[0]
            operator_code = match[1]
            band = match[2]
            channel = match[3]
            qnwinfo_info.append({
                'network_type': network_type,
                'operator_code': operator_code,
                'band': band,
                'channel': channel
            })

        return qnwinfo_info

    def serving_cell(self):
        response = self.send_at_command("AT+QENG=\"servingcell\"")

        # Define the regex pattern with named groups
        lte_pattern = (
            r'"LTE",'
            r'"(?P<is_tdd>[^"]+)",'  # Matches the is_tdd (quoted string)
            r'(?P<MCC>\d+),'  # Matches the MCC (digits)
            r'(?P<MNC>\d+),'  # Matches the MNC (digits)
            r'(?P<cellID>\d+),'  # Matches the cellID (digits)
            r'(?P<PCID>\d+),'  # Matches the PCID (digits)
            r'(?P<earfcn>\d+),'  # Matches the earfcn (digits)
            r'(?P<freq_band_ind>\d+),'  # Matches the freq_band_ind (digits)
            r'(?P<UL_bandwidth>\d+),'  # Matches the UL_bandwidth (digits)
            r'(?P<DL_bandwidth>\d+),'  # Matches the DL_bandwidth (digits)
            r'(?P<TAC>[A-Za-z0-9]+),'  # Matches the TAC (alphanumeric)
            r'(?P<RSRP>-?\d+),'  # Matches the RSRP (integer, can be negative)
            r'(?P<RSRQ>-?\d+),'  # Matches the RSRQ (integer, can be negative)
            r'(?P<RSSI>-?\d+),'  # Matches the RSSI (integer, can be negative)
            r'(?P<SINR>-?\d+),'  # Matches the SINR (integer, can be negative)
            r'(?P<CQI>\d+),'  # Matches the CQI (digits)
            r'(?P<tx_power>-?\d+|-),'  # Matches the tx_power (integer or "-")
            r'(?P<srxlev>-?\d+|-)'
            # r'(?P<srxlev>-?[^,]+)'          # Matches the srxlev (integer, can be negative)

        )

        nrnsa_pattern = (
            r'\+QENG: "NR5G-NSA",'  # Matches the initial part of the response
            r'(?P<MCC>\d+),'  # Matches the MCC (digits)
            r'(?P<MNC>\d+),'  # Matches the MNC (digits)
            r'(?P<PCID>\d+),'  # Matches the PCID (digits)
            r'(?P<RSRP>-?\d+),'  # Matches the RSRP (integer, can be negative)
            r'(?P<SINR>-?\d+),'  # Matches the SINR (integer, can be negative)
            r'(?P<RSRQ>-?\d+),'  # Matches the RSRQ (integer, can be negative)
            r'(?P<ARFCN>\d+),'  # Matches the ARFCN (digits)
            r'(?P<band>\w+),'  # Matches the band (alphanumeric)
            r'(?P<NR_DL_bandwidth>\d+),'  # Matches the NR_DL_bandwidth (digits)
            r'(?P<scs>\d+)'  # Matches the scs (digits)
        )

        nrsa_pattern = (
            r'"NR5G-SA",'  # Matches the initial part of the response
            r'"(?P<is_tdd>[^"]+)",'  # Matches the is_tdd (quoted string)
            r'(?P<MCC>\d+),'  # Matches the MCC (digits)
            r'(?P<MNC>\d+),'  # Matches the MNC (digits)
            r'(?P<cellID>\d+),'  # Matches the cellID (digits)
            r'(?P<PCID>\d+),'  # Matches the PCID (digits)
            r'(?P<TAC>[A-Za-z0-9]+),'  # Matches the TAC (alphanumeric)
            r'(?P<arfcn>\d+),'  # Matches the arfcn (digits)
            r'(?P<freq_band_ind>\d+),'  # Matches the freq_band_ind (digits)
            r'(?P<NR_DL_bandwidth>\d+),'  # Matches the NR_DL_bandwidth (digits)
            r'(?P<RSRP>-?\d+),'  # Matches the RSRP (integer, can be negative)
            r'(?P<RSRQ>-?\d+),'  # Matches the RSRQ (integer, can be negative)
            r'(?P<SINR>-?\d+),'  # Matches the SINR (integer, can be negative)
            r'(?P<scs>\d+)'  # Matches the scs (digits)
            r'(?P<srxlev>-?\d+)'  # Matches the srxlev (integer, can be negative)
        )

        # Check if a match is found and extract the values into variables
        values_lte = extract_values(lte_pattern, response)
        values_nr5g_nsa = extract_values(nrnsa_pattern, response)
        values_nr5g_sa = extract_values(nrsa_pattern, response)

        # Print the extracted values
        print('LTE Values:', values_lte)
        print('NR5G-NSA Values:', values_nr5g_nsa)
        print('NR5G-SA Values:', values_nr5g_sa)

        return response


def main(port='/dev/ttyUSB3',baud_rate=115200,command='AT',myapn='internet.vodafone.gr',camp_name=None,camp_id=0,exp_id=0):
    helper=Helper()
    my_modem = Modem()
    my_modem.initialize_port(port, baud_rate, 1)

    res = my_modem.is_alive()

    mode_pref = my_modem.get_prefered_mode()
    my_modem.set_prefered_mode("LTE:NR5G")

    oper, act = my_modem.get_oper_and_mode()

    #apn = my_modem.get_apn()
    #resp1 = my_modem.set_apn(myapn)
    rssi, ber = my_modem.get_csq()
    qrsrp_prx, qrsrp_drx, qrsrp_rx2, qrsrp_rx3, qrsrp_sysmode = my_modem.get_qrsrp()
    rsrq_prx, rsrq_drx, rsrq_rx2, rsrq_rx3, rsrq_sysmode = my_modem.get_qrsrq()
    sinr_prx, sinr_drx, sinr_rx2, sinr_rx3, sinr_sysmode = my_modem.get_qsinr()
    qnwinfo_info = my_modem.get_net_info()
    my_modem.serving_cell()

    if True:
        print(mode_pref)
        print(oper)
        print(act)
        #print(apn)
        #print(resp1)
        print(rssi)
        print(ber)
        print(qrsrp_prx, qrsrp_drx, qrsrp_rx2, qrsrp_rx3, qrsrp_sysmode)
        print(rsrq_prx, rsrq_drx, rsrq_rx2, rsrq_rx3, rsrq_sysmode)
        print(sinr_prx, sinr_drx, sinr_rx2, sinr_rx3, sinr_sysmode)
        print(qnwinfo_info)
        print("+++++++++++++++++++++++")

    print('(Physical) DBG: Completed serial physical measurements in parallel')

    mycsv_line = (
                    str(camp_name) + gparams._DELIMITER+
                    str(camp_id)+ gparams._DELIMITER+
                    str(exp_id)+ gparams._DELIMITER+
                    helper.get_str_timestamp() + gparams._DELIMITER +
                    str(mode_pref) + gparams._DELIMITER +
                    str(oper) + gparams._DELIMITER +
                    str(act) + gparams._DELIMITER +
                    str(None) + gparams._DELIMITER +
                    str(None) + gparams._DELIMITER +
                    str(rssi) + gparams._DELIMITER +
                    str(ber) + gparams._DELIMITER +
                    str(qrsrp_prx) + gparams._DELIMITER +
                    str(qrsrp_drx) + gparams._DELIMITER +
                    str(qrsrp_rx2) + gparams._DELIMITER +
                    str(qrsrp_rx3) + gparams._DELIMITER +
                    str(qrsrp_sysmode) + gparams._DELIMITER +
                    str(rsrq_prx) + gparams._DELIMITER +
                    str(rsrq_drx) + gparams._DELIMITER +
                    str(rsrq_rx2) + gparams._DELIMITER +
                    str(rsrq_rx3) + gparams._DELIMITER +
                    str(rsrq_sysmode) + gparams._DELIMITER +
                    str(sinr_prx) + gparams._DELIMITER +
                    str(sinr_drx) + gparams._DELIMITER  +
                    str(sinr_rx2) + gparams._DELIMITER +
                    str(sinr_rx3) + gparams._DELIMITER +
                    str(sinr_sysmode) )

    helper.write_db(loc=gparams._DB_FILE_LOC_OUTPUT_PHY, mystr=mycsv_line)

if __name__ == "__main__":
    try:
        while True:
            main(port='/dev/ttyUSB3', baud_rate=115200, command='AT', myapn='static.ipt', camp_name=None, camp_id=0,
             exp_id=0)
    except Exception as ex:
        print('(Physical) ERROR: Failed='+str(ex))