#!/usr/bin/python
#!/usr/bin/env python

import srt  # for srt format handling
import glob  # for unix style filename matching
import sys  # input arguments
import getopt  # to raise error in case of incorrect arguments


def main(argv):
    # Parse arguments
    fnames = 0
    primary_language = ''
    secondary_language = ''
    try:
        opts, args = getopt.getopt(
            argv, "hfp:s:o:", ["primary-language=", "secondary-language=","output-file="])
    except getopt.GetoptError:
        print ('merge_subtitles.py -f (use filenames) -p <primary_language>'
               '-s <secondary_language>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print ('merge_subtitles.py -p <primary_language>'
                   ' -s <secondary_language>')
            sys.exit()
        elif opt in ("-f"):
            fnames = 1
        elif opt in ("-p", "--primary-language"):
            primary_language = arg
        elif opt in ("-s", "--secondary-language"):
            secondary_language = arg
        elif opt in ("-o", "--output-file"):
            output = arg

    if (fnames == 0):        
        # Read files and convert to list
        primary_path = glob.glob('./*.' + primary_language + '.srt')[0]
        secondary_path = glob.glob('./*.' + secondary_language + '.srt')[0]
    else:
        primary_path = primary_language
        secondary_path = secondary_language
        
    primary_file = open(primary_path, 'r', errors='ignore')
    primary_text = primary_file.read()
    primary_file.close()
    secondary_file = open(secondary_path, 'r', errors='ignore')
    secondary_text = secondary_file.read()
    secondary_file.close()
    subtitle_generator_primary = srt.parse(primary_text)
    subtitles_primary = list(subtitle_generator_primary)
    subtitle_generator_secondary = srt.parse(secondary_text)
    subtitles_secondary = list(subtitle_generator_secondary)

    # Make primary yellow
    for s in subtitles_primary:
        s.content = '<font color="#ffff54">' + s.content + '</font>'

    # Place secondary on top
    for s in subtitles_secondary:
        s.content = '{\\an8}' + s.content

    # Merge
    subtitles_merged = subtitles_primary + subtitles_secondary
    subtitles_merged = list(srt.sort_and_reindex(subtitles_merged))

    if (output == None):
        # Write merged to file
        merged_path = primary_path.replace(primary_language, 'merged')
    else:
        merged_path = output
        
    merged_text = srt.compose(subtitles_merged)
    merged_file = open(merged_path, 'w')
    merged_file.write(merged_text)
    merged_file.close()


if __name__ == "__main__":
    main(sys.argv[1:])
