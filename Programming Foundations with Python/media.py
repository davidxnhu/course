import webbrowser
import video

class Movie(video.Video):
    def __init__(self,title,duration,storyline,poster_image,youtube_trailer):
        video.Video.__init__(self,title,duration)
        self.storyline=storyline
        self.poster_image_url=poster_image
        self.trailer_youtube_url=youtube_trailer
    def show_trailer(self):
        webbrowser.open(self.trailer_youtube_url)
        
    def show_info(self):
        print ("Title is "+self.title)
        print ("Duration is"+str(self.duration))
        self.show_trailer()        
