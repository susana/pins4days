# Pins4Days

A Google App Engine (standard) app written in Python for gathering up and displaying in one place all the messages your team has ever pinned.

**Why?**

Because channels have a max of 100 pins and if you've taken up the strategy of simply moving to a new channel when that happens, you might care to see your pins in a single place, conveniently. :)

**What's it going to cost?**

This is being implemented with the constraint that it only uses what's available in the [Google Cloud Platform (GCP) free tier](https://cloud.google.com/free/).

This app uses the following free tier GCP products:

- Google App Engine (for hosting and serving the app, and using shared memcache for user sessions)
- Google Cloud Datastore (for storing pins, attachments and users)
- Google Cloud Storage (for storing the app config)

### Installation

⚠️TODO

### Tests

From the root dir:

```shell
python runner.py /usr/local/opt/google-cloud-sdk/ --test-path=test
```

### TODO

I know, there's a lot that can be improved. I'll get to it one day.

- [ ] make a Slack API [request](https://api.slack.com/methods/channels.list) to get channels, keep in mem, poll occasionally to update
- [ ] read in and store existing pins from all channels
- [ ] tests
- [x] docstrings
- [ ] readme
- [ ] auth for api endpoint
- [ ] log out
- [ ] update dir structure
  - [ ] http://flask.pocoo.org/docs/0.12/views/
  - [x] create models/ dir
- [ ] refactor templates (i.e. reuse general HTML structure: common header, containers, etc)
- [ ] ⭐️ consider storing pins and deleting them as the pin events are sent from Slack to avoid ever hitting the 100 pin max
