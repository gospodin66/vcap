import cv2
import os
import time
import click


class Vcap:

    _VIDEOS_BASEDIR = './videos/'
    _TIME_FORMAT = "%Y-%m-%d %I:%M:%S %p"
    
    def __init__(self):
        if not os.path.exists(self._VIDEOS_BASEDIR):
            print("dir {self._VIDEOS_BASEDIR} doesn't exist - creating..")
            os.makedirs(self._VIDEOS_BASEDIR)


    #
    #
    #
    def init_backSub(self):
        self.algo = 'KNN' # KNN | MOG2

        if self.algo == 'MOG2':
            self.backSub = cv2.createBackgroundSubtractorMOG2()
        else:
            self.backSub = cv2.createBackgroundSubtractorKNN()


    #
    # init default vcap cnf to capture|play video
    # vfile => path of video file (src|dest - depends on mode)
    # mode  => mode to open videocap in:
    #       => cap  - open camera at index 0 (1st available)
    #       => play - open video file
    #
    def init_cap(self, vfile: str, mode: str) -> int:
        if vfile:
            path = vfile
        else:
            path = self._VIDEOS_BASEDIR+"default.mp4"
            
        if mode == "cap":
            self.cap = cv2.VideoCapture(0)
        elif mode == "play":
            self.cap = cv2.VideoCapture(path)
        else:
            print("invalid mode.")
            return 1

        return 0
    
    
    #
    #
    #
    def init_writer(self, vfile: str):
        if vfile:
            path = vfile
        else:
            path = self._VIDEOS_BASEDIR+"default.mp4"
        self.frame_cnf = {
            "name": path,
            "fourcc": cv2.VideoWriter_fourcc(*'mp4v'),
            "fps": 20.0,
            "frame_size": {
                "w": int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                "h": int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            },
        }
        self.vwriter = cv2.VideoWriter(
            self.frame_cnf["name"],
            self.frame_cnf["fourcc"],
            self.frame_cnf["fps"],
            (self.frame_cnf["frame_size"]["w"], self.frame_cnf["frame_size"]["h"])
        )


    #
    # caps video to provided path
    # dstpath => dest path of video file
    #
    # obj detection using Haar Cascade Classifier:
    # - Eyes
    # - Frontal Face
    # - Full Body
    # - Upper Body
    # - Lower Body
    # - Cats
    # - Stop Signs
    # - License Plates, etc.
    #
    @click.command()
    @click.option(
        '--dstpath',
        prompt='Destination path',
        help='Destination path of the video save.'
    )
    def cap_video(self, dstpath: str) -> int:
        """Simple program that captures video."""

        if not dstpath:
            click.echo("empty path.")
            return 1

        self.init_cap(dstpath, "cap")
        self.init_writer(dstpath)

        if (self.cap.isOpened() == False): 
            click.echo(f"Error opening video file: cap open = {self.cap.isOpened()}")
            return 1

        cascade_classifier_eyes = cv2.CascadeClassifier(f"{cv2.data.haarcascades}haarcascade_eye.xml")
        cascade_classifier_face = cv2.CascadeClassifier(f"{cv2.data.haarcascades}haarcascade_frontalface_alt.xml")

        framecnt = 0
        while 1:

            ret, frame = self.cap.read()

            if not ret:
                break

            click.echo(framecnt, end=" ", flush=True)

            t = time.strftime(self._TIME_FORMAT, time.localtime())
            frametxt = f"{t} :: {str(framecnt)}"

            cv2.putText(frame, frametxt, (20, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255))

            image_grey = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

            detected_eyes = cascade_classifier_eyes.detectMultiScale(image_grey, minSize=(30, 30))
            detected_faces = cascade_classifier_face.detectMultiScale(image_grey, minSize=(50, 50))

            if len(detected_eyes) != 0:
                for (x, y, width, height) in detected_eyes:
                    cv2.rectangle(frame, (x, y), (x + height, y + width), (0, 255, 0), 2)

            if len(detected_faces) != 0:
                for (x, y, width, height) in detected_faces:
                    cv2.rectangle(frame, (x, y), (x + height, y + width), (0, 0, 255), 2)

            cv2.imshow('TestFrame', frame)

            self.vwriter.write(frame)

            framecnt += 1

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        
        self.cap.release()
        self.vwriter.release()
        cv2.destroyAllWindows()
        return 0


    #
    # uses fgMask when playing video
    # srcpath => src path of video file
    #
    @click.command()
    @click.option(
        '--srcpath',
        prompt='Source path',
        help='Source path of the video to play.'
    )
    def play_video(self, srcpath: str) -> int:
        """Simple program that plays captured video."""

        if not srcpath:
            click.echo("empty path.")
            return 1

        self.init_cap(srcpath, "play")
        self.init_backSub()

        if (self.cap.isOpened() == False):
            print("Error opening video file")
            return 1
        
        while(self.cap.isOpened()):

            ret, frame = self.cap.read()

            if not ret:
                break
            
            fgMask = self.backSub.apply(frame)

            cv2.imshow('Frame', frame)
            cv2.imshow('FG Mask', fgMask)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
            
        cv2.destroyAllWindows()
        self.cap.release()
        return 0



@click.group()
def cli():
    pass


cli.add_command(Vcap.cap_video)
cli.add_command(Vcap.play_video)


if __name__ == '__main__':
    cli()
