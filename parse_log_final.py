
LOG_FILE = "C:\Users\Elinor Perl\Downloads\parser_2.3.log"
g_speed = 45
g_count = 0

def sum_bytes(bytes):
    sum = 0
    for byte in bytes:
        sum += ord(byte)
    return sum

def calc_fcs(data):
    fcs = 0xff-(sum_bytes(data)%0x100)
    print "CalcFCS: %s" % hex(fcs)
    return fcs

def parse_line(line):
    global g_speed
    global g_count
    bin_line = line.replace(' ', '').decode('hex')
    bin_line = bin_line.replace('\x7d\x5e', '\x7e')
    bin_line = bin_line.replace('\x7d\x5d', '\x7d')
    # Get header
    header = bin_line[:3]
    # Slice last bit
    bin_line = bin_line[:-1]
    # Get FCS
    fcs = bin_line[-1:]
    bin_line = bin_line[:-1]
    data = bin_line[3:]
    speed = round((((ord(data[2])&0b1111)<<8)+ord(data[1]))*0.1, 1)
    if calc_fcs(header[1:]+data) != ord(fcs):
        print "Speed: %s, Data: %s, FCS: %s" % (speed, repr(data), repr(fcs))
        print "FCS Wrong!"        
    if abs(g_speed-speed) > 5:
        print "Anomaly! %d g: %s s: %s d: %s" % (g_count, g_speed, speed, abs(g_speed-speed))
        g_count = 0

    else:
        g_speed = speed
        g_count += 1

def main():
    count = 1
    for line in open(LOG_FILE, 'rb').readlines():
        print ("Line: %d" % count)
        count += 1
        parse_line(line.strip())

if __name__ == "__main__":
    main()