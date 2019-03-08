from datetime import date

class Tweet:
    """A class tweet

    === Attributes ===
    content: the content of the tweet.
    userid: the id of the user who wrote the tweet.
    created_at: the date the tweet was written.
    likes: The number of likes the tweet has received.

    === Representation invariants ===
    len(content) <= 140

    >>> t1 = Tweet('Giovanni', date(2017, 9, 18), 'Hello')
    >>> len(t1.content) <= 140
    True
    """
    content: str
    userid: str
    created_at: date
    likes: int

    def __init__(self, who: str, when: date, what: str) -> None:
        self.content = what
        self.userid = who
        self.created_at = when
        self.likes = 0

    def like(self, num_likes: int):
        """like a tweet

        Precondition: num_;okes >= 0

        >>> t1 = Tweet('Giovanni', date(2017, 9, 18), 'Hello')
        >>> t1.likes
        0
        >>>t1.like(20)
        >>>t1.likes
        20
        """
        self.like += num_likes

if __name__ == '__main__':
    t1 = Tweet('Giovanni', date(2017, 9, 18), 'Hello')
    t2 = t1
    t2.content = 'goodbye'
    print(t1.content, t2.content)
