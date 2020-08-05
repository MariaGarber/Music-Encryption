
from bit_manipulation import lsb_interleave_bytes, lsb_deinterleave_bytes
import getopt
import math
import os
import sys
from time import time
import wave


def hide_data(sound_path, file_path, output_path, num_lsb):
    """Hide data from the file at file_path in the sound file at sound_path"""
    sound = wave.open(sound_path, "r")

    params = sound.getparams()
    num_channels = sound.getnchannels()
    sample_width = sound.getsampwidth()
    num_frames = sound.getnframes()
    num_samples = num_frames * num_channels

    # We can hide up to num_lsb bits in each sample of the sound file
    max_bytes_to_hide = (num_samples * num_lsb) // 8
    # Open File
    data = open(file_path, "r+b").read().decode()
    file_size = os.stat(file_path).st_size
    data = str(len(str(file_size) + " " + str(data))) + " " + str(data)
    print(data)
    file_size = len(data)
    data = data.encode()

    print("Using {} LSBs, we can hide {} B".format(num_lsb, max_bytes_to_hide))

    print("Reading files...".ljust(35), end='', flush=True)
    start = time()
    sound_frames = sound.readframes(num_frames)

    print("Done in {:.2f} s".format(time() - start))

    # Checks if the input file can be encrypted into the wav
    if file_size > max_bytes_to_hide:
        required_lsb = math.ceil(file_size * 8 / num_samples)
        raise ValueError("Input file too large to hide, "
                         "requires {} LSBs, using {}"
                         .format(required_lsb, num_lsb))

    if sample_width != 1 and sample_width != 2:
        # Python's wave module doesn't support higher sample widths
        raise ValueError("File has an unsupported bit-depth")

    print("Hiding {} bytes...".format(file_size).ljust(35), end='', flush=True)
    start = time()
    sound_frames = lsb_interleave_bytes(sound_frames, data, num_lsb,
                                        byte_depth=sample_width)
    print("Done in {:.2f} s".format(time() - start))

    print("Writing to output wav...".ljust(35), end='', flush=True)
    start = time()
    sound_steg = wave.open(output_path, "w")
    sound_steg.setparams(params)
    sound_steg.writeframes(sound_frames)
    sound_steg.close()
    print("Done in {:.2f} s".format(time() - start))


def recover_data(sound_path, output_path, num_lsb):
    """Recover data from the file at sound_path to the file at output_path"""
    print("Reading files...".ljust(35), end='', flush=True)
    start = time()
    sound = wave.open(sound_path, "r")
    # Here change
    num_channels = sound.getnchannels()
    sample_width = sound.getsampwidth()
    num_frames = sound.getnframes()
    sound_frames = sound.readframes(num_frames)

    print("Done in {:.2f} s".format(time() - start))

    if sample_width != 1 and sample_width != 2:
        # Python's wave module doesn't support higher sample widths
        raise ValueError("File has an unsupported bit-depth")

    # Added by Me :)
    bytes_to_recover = int(lsb_deinterleave_bytes(sound_frames, 8 * 3, num_lsb,
                                                  byte_depth=sample_width).decode())
    print("Recovering {} bytes...".format(bytes_to_recover).ljust(35),
          end='', flush=True)
    start = time()
    data = lsb_deinterleave_bytes(sound_frames, 8 * bytes_to_recover, num_lsb,
                                  byte_depth=sample_width)
    print("Done in {:.2f} s".format(time() - start))

    print("Writing to output file...".ljust(35), end='', flush=True)
    start = time()
    data = data[4::]
    output_file = open(output_path, "wb+")
    output_file.write(bytes(data))
    output_file.close()
    print("Done in {:.2f} s".format(time() - start))


def usage():
    print("\nCommand Line Arguments:\n",
          "-h, --hide        To hide data in a sound file\n",
          "-r, --recover     To recover data from a sound file\n",
          "-s, --sound=      Path to a .wav file\n",
          "-f, --file=       Path to a file to hide in the sound file\n",
          "-o, --output=     Path to an output file\n",
          "-n, --LSBs=       How many LSBs to use\n",
          "--help            Display this message\n")


if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hrs:f:o:n:b:',
                                   ['hide', 'recover', 'sound=', 'file=',
                                    'output=', 'LSBs=', 'bytes=', 'help'])
    except getopt.GetoptError:
        usage()
        sys.exit(1)

    hiding_data = False
    recovering_data = False
    num_bytes_to_recover = 0

    # file paths for input, sound, and output files
    sound_fp = ""
    input_fp = ""
    output_fp = ""

    # number of least significant bits to alter when hiding/recovering data
    num_bits = 2

    for opt, arg in opts:
        if opt in ("-h", "--hide"):
            hiding_data = True
        elif opt in ("-r", "--recover"):
            recovering_data = True
        elif opt in ("-s", "--sound"):
            sound_fp = arg
        elif opt in ("-f", "--file"):
            input_fp = arg
        elif opt in ("-o", "--output"):
            output_fp = arg
        elif opt in ("-n", "--LSBs="):
            num_bits = int(arg)
        elif opt == "--help":
            usage()
            sys.exit(1)
        else:
            print("Invalid argument {}".format(opt))

    try:
        if hiding_data:
            hide_data(sound_fp, input_fp, output_fp, num_bits)
        if recovering_data:
            recover_data(sound_fp, output_fp, num_bits)
    except Exception as e:
        print("Ran into an error during execution.\n",
              "Check input and try again.\n")
        print(e)
        usage()
        sys.exit(1)
