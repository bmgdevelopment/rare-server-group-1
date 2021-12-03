CREATE TABLE 'Users' (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'first_name' varchar,
    'last_name' varchar,
    'email' varchar,
    'bio' varchar,
    'username' varchar,
    'password' varchar,
    'profile_image_url' varchar,
    'created_on' date,
    'active' bit,
    'is_staff' bit
);

CREATE TABLE 'DemotionQueue' (
    'action' varchar,
    'admin_id' INTEGER,
    'approver_one_id' INTEGER,
    FOREIGN KEY(`admin_id`) REFERENCES `Users`(`id`),
    FOREIGN KEY(`approver_one_id`) REFERENCES `Users`(`id`),
    PRIMARY KEY (action, admin_id, approver_one_id)
);

CREATE TABLE 'Subscriptions' (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'follower_id' INTEGER,
    'author_id' INTEGER,
    'created_on' date,
    'ended_on' date,
    FOREIGN KEY(`follower_id`) REFERENCES `Users`(`id`),
    FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE 'Posts' (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'user_id' INTEGER,
    'category_id' INTEGER,
    'title' varchar,
    'publication_date' date,
    'image_url' varchar,
    'content' varchar,
    'approved' bit
);

CREATE TABLE 'Comments' (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'post_id' INTEGER,
    'author_id' INTEGER,
    'content' varchar,
    'created_on' date,
    FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
    FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE 'Reactions' (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'label' varchar,
    'image_url' varchar
);

CREATE TABLE 'PostReactions' (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'user_id' INTEGER,
    'reaction_id' INTEGER,
    'post_id' INTEGER,
    FOREIGN KEY(`user_id`) REFERENCES `Users`(`id`),
    FOREIGN KEY(`reaction_id`) REFERENCES `Reactions`(`id`),
    FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`)
);

CREATE TABLE 'Tags' (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'label' varchar
);

CREATE TABLE 'PostTags' (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'post_id' INTEGER,
    'tag_id' INTEGER,
    FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
    FOREIGN KEY(`tag_id`) REFERENCES `Tags`(`id`)
);

CREATE TABLE 'Categories' (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'label' varchar
);


-- Categories Insert
INSERT INTO Categories ('label') VALUES ('News');
INSERT INTO Categories ('label') VALUES ('Entertainment');
INSERT INTO Categories ('label') VALUES ('Comedy');
INSERT INTO Categories ('label') VALUES ('Advice');
INSERT INTO Categories ('label') VALUES ('SaturdayTest');

-- Tags Insert
INSERT INTO Tags ('label') VALUES ('JavaScript');
INSERT INTO Tags ('label') VALUES ('React.js');
INSERT INTO Tags ('label') VALUES ('Python');

-- Reactions Insert
INSERT INTO Reactions ('label', 'image_url') VALUES ('happy', 'https://pngtree.com/so/happy');

-- Users Insert
INSERT INTO `Users` VALUES (null, 'Melody', 'Barker', 'melb@gmail.com', null, 'melb@gmail.com', '123', 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png', '2021-11-19', true, true);
INSERT INTO `Users` VALUES (null, 'Sam', 'Baker', 'samb@gmail.com', null, 'samb@gmail.com', '123', 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png', '2021-11-19', true, false);
INSERT INTO `Users` VALUES (null, 'Brittany', 'Garrett', 'bmg@gmail.com', null, 'bmg@gmail.com', '123', 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png', '2021-11-19', true, false);
INSERT INTO `Users` VALUES (null, 'Stephanie', 'Hamilton', 'stephanieh@gmail.com', null, 'steohanieh@gmail.com', '123', 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png', '2021-11-19', true, false);
INSERT INTO `Users` VALUES (null, 'Blake', 'McAdams', 'blakem@gmail.com', null, 'blakemb@gmail.com', '123', 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png', '2021-11-19', true, true);

-- DemotionQueue Insert
INSERT INTO DemotionQueue VALUES ('No Action', 1, 1);

-- Subscriptions Insert
INSERT INTO Subscriptions VALUES (null, 1, 2, '20211113', 'current subscription' );

-- Comments Insert
INSERT INTO Comments VALUES (null, 2, 3, 'New comment for post', '2021112');

-- PostReactions Insert
INSERT INTO PostReactions VALUES (null, 2, 2, 3)

-- Posts Insert
INSERT INTO Posts VALUES (null, 1, 1, 'title1', 20211114, 'url1', 'content1', true);
INSERT INTO Posts VALUES (null, 3, 1, 'title2', 20211116, 'url2', 'content2', false);
INSERT INTO Posts VALUES (null, 2, 1,'title3', 20211120, 'url3', 'content3', true);

-- Post Tags
INSERT INTO PostTags VALUES (null, 2, 1);

UPDATE users
SET is_staff = True
WHERE is_staff = 'true'

SELECT * FROM Users

SELECT * FROM Posts
 

 
DROP TABLE Users