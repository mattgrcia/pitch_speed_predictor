import gif_rename
import gif_to_pic
import subprocess as sp
import pandas as pd
import pitcher_detector
import scrape_gifs
import re
import time


def main():
    start = time.time()

    # Convert the SQLit3 database to a Pandas dataframe.
    df = pd.read_csv('pitcher_list.csv')

    # Add the PitcherList link for each pitcher.
    df['Link'] = 'http://pitcherlist.com/pitcher/' \
                 + df['Pitcher'].str.lower().str.split().str[0] + '-' \
                 + df['Pitcher'].str.lower().str.split().str[1]

    # Create a master list to hold info on all pitches.
    all_pitches_info = []

    # For each pitcher,
    for item in df['Link']:

        # find all Gfycat terms, specific pitches, and pitch speeds.
        scrapes = sel.terms(str(item))

        # Either we have a valid link...*
        if scrapes:
            terms = scrapes[0]
            pitches = scrapes[1]
            speeds = scrapes[2]
            ages = scrapes[3]

            # For each of that pitcher's pitches,
            for idx, term in enumerate(terms):

                # save a gif of the pitch as a .webm file from Gfycat,
                gfy.save(term)

                # convert that .webm file to a .gif file,
                sp.call(['ffmpeg', '-i', '%s.webm' % term, '%s.gif' % term])

                # and save the first and last frames of the gif as .png files.
                gif.frames('%s.gif' % term, term, '')

                # Then, create a list of pitch-specific info.
                pitch_info = []

                # In that list, add

                # the pitcher's name for later indexing purposes,
                pitch_info.append(item)

                # the pitcher's age,
                pitch_info.append(ages[idx])

                # the position data,
                try:
                    start_positional_data = finder.position('0_%s.png' % term)
                    end_positional_data = finder.position('1_%s.png' % term)
                    x_start = (start_positional_data[0] + start_positional_data[2]) / 2
                    x_end = (end_positional_data[0] + end_positional_data[2]) / 2
                    width_start = start_positional_data[2] - start_positional_data[0]
                    width_end = end_positional_data[2] - end_positional_data[0]
                    width_average = (width_start + width_end) / 2
                    x_change = (abs(x_end - x_start)) / width_average
                    pitch_info.append(x_change)

                    # the pitch name,
                    pitch_info.append(pitches[idx])

                    # and the pitch speed.
                    pitch_info.append(speeds[idx])

                    # Then add this list of pitch info back to the master.
                    all_pitches_info.append(pitch_info)

                    # Let's remove the files we used, so we do not end up with a thousand files.
                    sp.call(['rm', '%s.webm' % term])
                    sp.call(['rm', '%s.gif' % term])
                    sp.call(['rm', '0_%s.png' % term])
                    sp.call(['rm', '1_%s.png' % term])

                # (Just making sure we don't break on a pitcher that doesn't get valid positional data).
                except UnboundLocalError:
                    break

    # Let's change the links back to the pitcher's name for later integration.
    for pitch in all_pitches_info:
        pitch[0] = str(re.findall('pitcher/(.*)-', pitch[0])[0]).title() + ' ' \
                  + str(re.findall('-(.*)', pitch[0])[0]).title()

    # Put all the information into a Pandas dataframe in preparation for modeling.
    pitcher_name = []
    pitcher_age = []
    movement = []
    pitch_type = []
    pitch_speed = []

    for pitch in all_pitches_info:
        pitcher_name.append(pitch[0])
        pitcher_age.append(pitch[1])
        movement.append(pitch[2])
        pitch_type.append(pitch[3])
        pitch_speed.append(pitch[4])

    pitcher_movement = pd.DataFrame()
    pitcher_movement['pitcher_name'] = pitcher_name
    pitcher_movement['pitcher_age'] = pitcher_age
    pitcher_movement['movement'] = movement
    pitcher_movement['pitch_type'] = pitch_type
    pitcher_movement['pitch_speed'] = pitch_speed

    # Export the dataframe to a csv file for continued and external use.
    pitcher_movement.to_csv('pitcher_movement.csv')

    end = time.time()
    print(end - start)


if __name__ == '__main__':
    main()
