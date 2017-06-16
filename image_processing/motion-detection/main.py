import cv2, time
from datetime import datetime as dt
from pandas import DataFrame as DF

def write_log(entries):
    """

    :param entries:         A list of (start, end) pairs representing the start and end times of an object
                        begin in the frame. Every entry is a dictionary of the format:

                                    "Start":    <start_time> (datetime object)
                                    "End":      <end_time>   (datetime object)
    :return:            -
    """
    df = DF(columns=["Start", "End"])

    for entry in entries:
        df = df.append(entry, ignore_index=True)

    df.to_csv("log.csv")

def process_frame(reference_frame, current_frame, color_frame):
    """

    :param reference_frame:       The reference frame, used for calculating deltas, etc.
    :param current_frame:         The frame to be processed
    :param color_frame:           The color frame over which we add the rectangles
    :return:                      The processed frame
                                  The status = True if object in the frame
                                               False otherwise
    """

    status = False

    delta_frame = cv2.absdiff(reference_frame, current_frame)

    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    (_, cnts, _) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        status = True # we have object in the frame
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(color_frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    return color_frame, status

def start_capture(stream, exit_key='q'):
    """

    :param stream:          A cv2.VideoCapture object used for the video stream
    :param exit_key:        The key for exiting the video capture --- default: 'q'
    :return:                -
    """

    reference_frame = None
    status = False
    start_time = None
    end_time = None
    entries = []

    while(True):
        _, current_frame = stream.read()

        gray_frame = cv2.cvtColor(current_frame,
                                  cv2.COLOR_BGR2GRAY)

        gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

        if reference_frame is None:
            # We are at the 1st frame
            reference_frame = gray_frame
            continue

        frame, new_status = process_frame(reference_frame, gray_frame, current_frame)

        if new_status and (not status):
            #an object entered the video
            start_time = dt.now()

        if (not new_status) and status:
            #the object no longer in the frame
            end_time = dt.now()
            entries.append({
                "Start": start_time,
                "End":  end_time
            })

        status = new_status

        cv2.imshow("Capturing...", frame)
        key = cv2.waitKey(1)
        if key == ord(exit_key):
            if status:
                entries.append({
                    "Start": start_time,
                    "End": dt.now()
                })
            break

    return entries

def main():
    video = cv2.VideoCapture(0)
    time.sleep(2)
    entries = start_capture(video)
    video.release()
    cv2.destroyAllWindows()
    write_log(entries)

if __name__ == "__main__":
    main()


