INSERT INTO Subscriber (username, email, PASSWORD) VALUES
('user1', 'user1@example.com', 'password1'),
('user2', 'user2@example.com', 'password2'),
('user3', 'user3@example.com', 'password3');

INSERT INTO Artist (NAME) VALUES
('Drake'),
('NF'),
('Halsey'),
('HIM'),
('Eminem'),
('Adele'),
('Linkin Park')
;

INSERT INTO Genre (genre_name) VALUES
('Rock'),
('Pop'),
('Jazz'),
('Rap')
;

INSERT INTO Album (NAME) VALUES
('Hope'),
('The Marshall Mathers LP'),
('Encore'),
('Dark Light'),
('Hybrid Theory'),
('Scorpion')
;

INSERT INTO Song (album_id, NAME, length) VALUES
(1, 'HOPE', 210),
(1, 'SUFFICE', 180),
(1, 'MISTAKE', 100),
(1, 'CAREFUL', 200),
(2, 'Kill You', 180),
(2, 'Stan', 320),
(2, 'The Real Slim Shady', 190),
(2, 'Marshall Mathers', 220),
(3, 'Puke', 230),
(3, 'Never Enough', 180),
(3, 'Rain Man', 200),
(4, 'Vapire Heart', 320),
(4, 'Killing Loneliness', 196),
(4, 'Dark Light', 235),
(5, 'Runaway', 200),
(5, 'Forgotten', 320),
(5, 'By Myself', 330),
(6, 'Survival', 200),
(6, 'Nonstop', 230),
(6, 'Emptionless', 100),

(NULL, "Without Me", 190),
(NULL, "Closer", 200),
(NULL, "Set Fire to the Rain", 190),
(NULL, "Someone Like You", 210)

;


INSERT INTO Song_artist (song_id, artist_id) VALUES
(1, 2),
(2, 2),
(3, 2),
(4, 2),

(5, 5),
(6, 5),
(7, 5),
(8, 5),

(9, 5),
(10, 5),
(11, 5),

(12, 4),
(13, 4),
(14, 4),

(15, 7),
(16, 7),
(17, 7),

(18, 1),
(19, 1),
(20, 1),

(21, 3),
(22, 3),
(23, 6),
(24, 6)
;


INSERT INTO Song_genre (song_id, genre_id) VALUES
(1, 4),
(2, 4),
(3, 4),
(4, 4),

(5, 4),
(6, 4),
(7, 4),
(8, 4),

(9, 4),
(10, 4),
(11, 4),

(12, 1),
(13, 1),
(14, 1),

(15, 1),
(16, 1),
(17, 1),

(18, 1),
(19, 1),
(20, 1),

(21, 2),
(22, 2),
(23, 2),
(24, 2)
;

INSERT INTO Artist_genre (artist_id, genre_id) VALUES
(1, 4),
(2, 4),
(3, 2),
(4, 1),
(5, 4),
(6, 2),
(7, 2)
;


INSERT INTO Album_artist (album_id, artist_id) VALUES
(1, 2),
(2, 5),
(3, 5),
(4, 4),
(5, 7),
(6, 1)
;

INSERT INTO Likes (username, song_id) VALUES
('user1', 1),
('user1', 2),
('user1', 3),
('user1', 4),
('user1', 5),
('user1', 6),
('user1', 7),
('user1', 9),
('user1', 10),
('user1', 12),
('user1', 14),
('user1', 15),
('user1', 16),
('user1', 17),
('user1', 21),
('user1', 22),
('user1', 23),
('user1', 24),

('user2', 2),
('user2', 9),
('user2', 10),
('user2', 12),
('user2', 14),
('user2', 15),
('user2', 13),
('user2', 20),
('user2', 4),
('user2', 22),
('user2', 23),


('user3', 1),
('user3', 24),
('user3', 10),
('user3', 11)
;




INSERT INTO Playlist (username, NAME) VALUES
('user1', 'EminemBest'),
('user2', 'Pop'),
('user3', 'Rock')
;


INSERT INTO Playlist_song (playlist_id, song_id) VALUES
(1, 5),
(1, 7),
(1, 8)
;