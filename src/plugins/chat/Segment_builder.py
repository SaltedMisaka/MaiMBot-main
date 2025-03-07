from typing import Dict, List, Union, Optional, Any
import base64
import os

"""
OneBot v11 Message Segment Builder

This module provides classes for building message segments that conform to the
OneBot v11 standard. These segments can be used to construct complex messages
for sending through bots that implement the OneBot interface.
"""



class Segment:
    """Base class for all message segments."""
    
    def __init__(self, type_: str, data: Dict[str, Any]):
        self.type = type_
        self.data = data
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the segment to a dictionary format."""
        return {
            "type": self.type,
            "data": self.data
        }


class Text(Segment):
    """Text message segment."""
    
    def __init__(self, text: str):
        super().__init__("text", {"text": text})


class Face(Segment):
    """Face/emoji message segment."""
    
    def __init__(self, face_id: int):
        super().__init__("face", {"id": str(face_id)})


class Image(Segment):
    """Image message segment."""
    
    @classmethod
    def from_url(cls, url: str) -> 'Image':
        """Create an Image segment from a URL."""
        return cls(url=url)
    
    @classmethod
    def from_path(cls, path: str) -> 'Image':
        """Create an Image segment from a file path."""
        with open(path, 'rb') as f:
            file_b64 = base64.b64encode(f.read()).decode('utf-8')
        return cls(file=f"base64://{file_b64}")
    
    def __init__(self, file: str = None, url: str = None, cache: bool = True):
        data = {}
        if file:
            data["file"] = file
        if url:
            data["url"] = url
        if not cache:
            data["cache"] = "0"
        super().__init__("image", data)


class At(Segment):
    """@Someone message segment."""
    
    def __init__(self, user_id: Union[int, str]):
        data = {"qq": str(user_id)}
        super().__init__("at", data)


class Record(Segment):
    """Voice message segment."""
    
    def __init__(self, file: str, magic: bool = False, cache: bool = True):
        data = {"file": file}
        if magic:
            data["magic"] = "1"
        if not cache:
            data["cache"] = "0"
        super().__init__("record", data)


class Video(Segment):
    """Video message segment."""
    
    def __init__(self, file: str):
        super().__init__("video", {"file": file})


class Reply(Segment):
    """Reply message segment."""
    
    def __init__(self, message_id: int):
        super().__init__("reply", {"id": str(message_id)})


class MessageBuilder:
    """Helper class for building complex messages."""
    
    def __init__(self):
        self.segments: List[Segment] = []
    
    def text(self, text: str) -> 'MessageBuilder':
        """Add a text segment."""
        self.segments.append(Text(text))
        return self
    
    def face(self, face_id: int) -> 'MessageBuilder':
        """Add a face/emoji segment."""
        self.segments.append(Face(face_id))
        return self
    
    def image(self, file: str = None) -> 'MessageBuilder':
        """Add an image segment."""
        self.segments.append(Image(file=file))
        return self
    
    def at(self, user_id: Union[int, str]) -> 'MessageBuilder':
        """Add an @someone segment."""
        self.segments.append(At(user_id))
        return self
    
    def record(self, file: str, magic: bool = False) -> 'MessageBuilder':
        """Add a voice record segment."""
        self.segments.append(Record(file, magic))
        return self
    
    def video(self, file: str) -> 'MessageBuilder':
        """Add a video segment."""
        self.segments.append(Video(file))
        return self
    
    def reply(self, message_id: int) -> 'MessageBuilder':
        """Add a reply segment."""
        self.segments.append(Reply(message_id))
        return self
    
    def build(self) -> List[Dict[str, Any]]:
        """Build the message into a list of segment dictionaries."""
        return [segment.to_dict() for segment in self.segments]


'''Convenience functions
def text(content: str) -> Dict[str, Any]:
    """Create a text message segment."""
    return Text(content).to_dict()

def image_url(url: str) -> Dict[str, Any]:
    """Create an image message segment from URL."""
    return Image.from_url(url).to_dict()

def image_path(path: str) -> Dict[str, Any]:
    """Create an image message segment from file path."""
    return Image.from_path(path).to_dict()

def at(user_id: Union[int, str]) -> Dict[str, Any]:
    """Create an @someone message segment."""
    return At(user_id).to_dict()'''