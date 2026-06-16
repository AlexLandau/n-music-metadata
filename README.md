# n-music-metadata

Find the data for each game in the [processed folder](processed).

This project exists to collect certain information from Nintendo Music in one place in an easily scriptable format. It
does not allow users to listen to music or otherwise bypass the need for a Nintendo Switch Online subscription.

Mostly this exists because I think certain nerds would like the information Nintendo Music provides about the "official"
names of different music tracks in different languages, and organizing it in this way is a nicer way to see it all than
manually flipping through each language in the app. (As it turns out, many games effectively only have Japanese and
English track titles -- understandably, as these track titles are rarely shown to a player in-game -- but see Mario Kart
World for an example where most tracks are translated into each language.)

Known issues:

- "Special playlists" not associated with "games", such as the preview playlist of the Nintendo Switch 2 version of
  Star Fox, are not currently included.

### Contributions

I will probably not be accepting any pull requests, but let me know in GitHub Issues if you have a use case for other
available metadata (links to pages on the Nintendo Music website? links to images?) or the data needs attention. The
repo should automatically check for updates twice a week.

Be warned that running these scripts yourself will download about 100 MB and put about 2 GB of files on your disk (at
time of writing) -- the "processed" information is *much* more compact, so I'd rather have that version be useful for
people.

### Legal notice

This is an unofficial, one-man project with no connection to Nintendo or its affiliates or any other developers or
rightsholders. Nintendo, Nintendo Music, Nintendo Switch Online, and all other trademarks referenced by the names in
this metadata are the property of Nintendo Co., Ltd., its subsidiaries and/or affiliates, and/or other developers or
rightsholders.
