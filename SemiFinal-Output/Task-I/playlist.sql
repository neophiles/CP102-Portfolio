# Create database
CREATE DATABASE playlist;

# Use database
Use playlist;

# Create table that will store user data
CREATE TABLE Users (
id VARCHAR (50) PRIMARY KEY NOT NULL,
name VARCHAR (50) NOT NULL,
password VARCHAR (10) NOT NULL,
email VARCHAR (50) NOT NULL
);

# Create table that will store playlist details
CREATE TABLE Playlist_Details (
id VARCHAR (50) PRIMARY KEY NOT NULL,
name VARCHAR (50) NOT NULL,
user_id VARCHAR (50) NOT NULL,
created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
);

# Create table that will store song details
CREATE TABLE Songs (
id VARCHAR (50) PRIMARY KEY NOT NULL,
title VARCHAR (50) NOT NULL,
artist VARCHAR (50) NOT NULL,
genre VARCHAR (50) NOT NULL
);

# Create table that will store the songs of playlists
CREATE TABLE Playlist_Songs (
playlist_id VARCHAR (50) NOT NULL,
song_id VARCHAR (50) NOT NULL,
FOREIGN KEY (playlist_id) REFERENCES Playlist_Details(id) ON DELETE CASCADE,
FOREIGN KEY (song_id) REFERENCES Songs(id) ON DELETE CASCADE
);

# Insert users
INSERT INTO Users (id, name, password, email) VALUES
('USR-0172', 'Neil', 'abcd1234', 'neil@gmail.com'),
('USR-0038', 'Samson', 'password', 'samson@yahoo.com'),
('USR-0195', 'Nathalie', 'abcd1234', 'nnjv@gmail.com'),
('USR-0084', 'Juan Dela Cruz', 'halimaw', 'jd.cruz@gmail.com'),
('USR-0267', 'Nico', 'abcd', 'niconico@outlook.com'),
('USR-0146', 'Vincent', '1234', 'vincent@gmail.com'),
('USR-0099', 'Ace', '1234567890', 'ace@yahoo.com'),
('USR-0301', 'Kyla', 'potato', 'kyla@gmail.com'),
('USR-0113', 'Faith', 'cool123', 'faith@gmail.com'),
('USR-0055', 'Marco', 'pass1234', 'marco@outlook.com');

# Insert songs to be available
INSERT INTO Songs (id, title, artist, genre) VALUES
('SNG-0147', 'Martyr Nyebera', 'Kamikazee', 'OPM Rock'),
('SNG-0059', 'Migraine', 'Moonstar88', 'OPM Rock'),
('SNG-0213', 'Oo', 'Up Dharma Down', 'Alternative Rock'),
('SNG-0088', 'Huwag Na Huwag Mong Sasabihin', 'Kitchie Nadal', 'Alternative Rock'),
('SNG-0032', 'Overdrive', 'Eraserheads', 'Alternative Rock'),
('SNG-0176', 'Tibok', 'Earl Agustin', 'Pop'),
('SNG-0264', 'Raining in Manila', 'Lola Amour', 'City Pop'),
('SNG-0111', 'Patutunguhan', 'Cup of Joe', 'Pop'),
('SNG-0074', 'Hey Barbara', 'IV of Spades', 'Funk Rock'),
('SNG-0192', 'Hinahanap-Hanap Kita', 'Rivermaya', 'Alternative Rock'),
('SNG-0225', 'Star Treatment', 'Arctic Monkeys', 'Indie Rock'),
('SNG-0004', 'Baby', 'Justin Bieber', 'Pop'),
('SNG-0303', 'The Real Slim Shady', 'Eminem', 'Hip-Hop'),
('SNG-0129', 'Groundhog''s Day', 'Primus', 'Funk Metal'),
('SNG-0188', 'Good Thing', 'Sure Sure', 'Indie'),
('SNG-0155', '14', 'Silent Sanctuary', 'Alternative Rock');

# Insert playlists of users
INSERT INTO Playlist_Details (id, name, user_id) VALUES
('LST-0321', 'Chill Vibes', 'USR-0172'),
('LST-0057', 'Rock Anthems', 'USR-0038'),
('LST-0189', 'OPM Favorites', 'USR-0195'),
('LST-0104', 'Sad Songs', 'USR-0084'),
('LST-0273', 'Workout Jams', 'USR-0267'),
('LST-0136', 'Throwback Hits', 'USR-0146'),
('LST-0222', 'Primus Power', 'USR-0099'),
('LST-0066', 'Love Songs', 'USR-0301'),
('LST-0315', 'Eminem Vibes', 'USR-0113'),
('LST-0090', 'Indie Discoveries', 'USR-0055');

# Insert songs into playlists
INSERT INTO Playlist_Songs (playlist_id, song_id) VALUES
('LST-0057', 'SNG-0147'),
('LST-0057', 'SNG-0059'),
('LST-0189', 'SNG-0213'),
('LST-0189', 'SNG-0088'),
('LST-0104', 'SNG-0176'),
('LST-0273', 'SNG-0303'),
('LST-0273', 'SNG-0129'),
('LST-0136', 'SNG-0032'),
('LST-0222', 'SNG-0129'),
('LST-0066', 'SNG-0004'),
('LST-0315', 'SNG-0303'),
('LST-0090', 'SNG-0225');

# Update the email of a user (Neil)
UPDATE Users
SET email = 'neil_updated@gmail.com'
WHERE id = 'USR-0172';

# Update the genre of a song
UPDATE Songs
SET genre = 'Indie Pop'
WHERE id = 'SNG-0059';

# Update the name of a playlist
UPDATE Playlist_Details
SET name = 'Chill Vibes Updated'
WHERE id = 'LST-0321';

# Delete a user (Samson)
DELETE FROM Users
WHERE id = 'USR-0038';

# Delete a song (Baby by Justin Bieber)
DELETE FROM Songs
WHERE id = 'SNG-0004';

# Delete playlist (Eminem Vibes)
DELETE FROM Playlist_Details
WHERE id = 'LST-0315';

# Delete a song from a playlist (Migraine from Rock Anthems)
DELETE FROM Playlist_Songs
WHERE playlist_id = 'LST-0057' AND song_id = 'SNG-0059';

# Get all songs in a specific playlist (Rock Anthems)
SELECT s.title, s.artist, s.genre FROM Songs s
JOIN Playlist_Songs ps ON s.id = ps.song_id
JOIN Playlist_Details pd ON ps.playlist_id = pd.id
WHERE pd.name = 'Rock Anthems';

# Get all users with Gmail addresses
SELECT * FROM Users WHERE email LIKE '%@gmail.com';

# List all playlists ordered by name (alphabetical)
SELECT id, name, user_id FROM Playlist_Details ORDER BY name ASC;

# Find all Pop songs
SELECT id, title, artist FROM Songs WHERE genre = 'Pop';

# Find all playlists owned by a user (Nico)
SELECT pd.id, pd.name FROM Playlist_Details pd
JOIN Users u ON pd.user_id = u.id
WHERE u.name = 'Nico';