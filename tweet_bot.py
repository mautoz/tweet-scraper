import tweepy
from datetime import datetime, timedelta
import pytz
import os
import textwrap

from dotenv import load_dotenv

load_dotenv()

MAX_LENGTH = 1500


class TweetScraper:
    def __init__(self) -> None:
        self._auth = tweepy.OAuthHandler(
            str(os.getenv("CONSUMER_KEY")), str(os.getenv("CONSUMER_SECRET"))
        )
        self._auth.set_access_token(
            str(os.getenv("ACCESS_KEY")), str(os.getenv("ACCESS_SECRET"))
        )

        # Creating an API object
        self._api = tweepy.API(self._auth)

    def get_tweets(self, profile: str) -> list:
        new_tweets = tweepy.Cursor(
            self._api.user_timeline, screen_name=profile, tweet_mode="extended"
        ).items(15)
        today = datetime.now(tz=pytz.UTC)
        start_date = today - timedelta(days=1)

        tweets = f"\u200bÚtimos tweets do perfil **{profile}**\n"
        for tweet in new_tweets:
            if tweet.created_at <= start_date:
                text = tweet._json["full_text"]

                buffer = textwrap.dedent(f"""
                \u200b{text}\n
                \u200bPublicação: {tweet.created_at}\n
                """)

                if hasattr(tweet, 'retweeted_status'):
                    tweet_url = f"https://twitter.com/{tweet.retweeted_status.user.screen_name}/status/{tweet.retweeted_status.id}"
                else:
                    tweet_url = f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}"

                buffer += textwrap.dedent(f"""
                \u200bLink original: {tweet_url}\n
                """)

                if len(tweets) + len(buffer) < MAX_LENGTH:
                    tweets += buffer

                else:
                    print(tweets)
                    tweets = buffer

        print(tweets)


if __name__ == "__main__":
    # Example of use
    tweet_scraper = TweetScraper()
    tweet_scraper.get_tweets("DCOfficial")
