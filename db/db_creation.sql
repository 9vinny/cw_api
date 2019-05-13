CREATE DATABASE IF NOT EXISTS charity_wallet;

use charity_wallet;

CREATE TABLE IF NOT EXISTS donor (
    donor_id INTEGER AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL UNIQUE,
    activation_date DATETIME NOT NULL,
    donation_cycle_start_date DATETIME,
    last_logged_in DATETIME,
    password VARCHAR(255) NOT NULL,
    lifetime_donation FLOAT NOT NULL DEFAULT '0.00',
    monthly_collected FLOAT NOT NULL DEFAULT '0.00',
    fav_causes VARCHAR(255),
    account_status BOOLEAN NOT NULL,
    plaid_item_id VARCHAR(255),
    plaid_access_token VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS charity (
    charity_id INTEGER AUTO_INCREMENT PRIMARY KEY,
    char_name VARCHAR(255) NOT NULL UNIQUE,
    char_desc VARCHAR(900),
    char_image VARCHAR(255),
    char_address VARCHAR(255),
    char_city VARCHAR(255),
    char_state VARCHAR(255),
    activation_date DATETIME NOT NULL ,
    last_logged_in DATETIME,
    charity_login VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    active_drives INTEGER,
    causes VARCHAR(255) NOT NULL,
    charity_type VARCHAR(255) NOT NULL,
    charity_nav_score FLOAT,
    tax_deductible BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS drive (
    drive_id INTEGER AUTO_INCREMENT PRIMARY KEY,
    charity_id INTEGER REFERENCES charity(char_id),
    name VARCHAR(255) NOT NULL,
    drive_desc VARCHAR(900),
    drive_image VARCHAR(255),
    target_amt FLOAT,
    collected_amt FLOAT,
    drive_city VARCHAR(255),
    drive_state VARCHAR(255),
    begin_date DATETIME,
    end_date DATETIME,
    active_status BOOLEAN NOT NULL,
    causes VARCHAR(255) NOT NULL,
    activation_date DATETIME NOT NULL,
    is_default BOOLEAN NOT NULL
);


CREATE TABLE IF NOT EXISTS drive_update (
    upd_id INTEGER AUTO_INCREMENT PRIMARY KEY,
    drive_id INTEGER REFERENCES drive(drive_id),
    drive_update VARCHAR(255) UNIQUE,
    activation_date DATETIME NOT NULL,
    update_image VARCHAR(255) UNIQUE
);


CREATE TABLE IF NOT EXISTS donor_drive (
    drive_id INTEGER REFERENCES drive(drive_id),
    donor_id INTEGER REFERENCES donor(donor_id),
    charity_id INTEGER REFERENCES charity(char_id),
    activation_date DATETIME NOT NULL,
    status BOOLEAN NOT NULL
);

ALTER TABLE donor_drive ADD CONSTRAINT PRIMARY KEY (drive_id, donor_id, charity_id);


CREATE TABLE IF NOT EXISTS plaid_transaction (
    transaction_id INTEGER AUTO_INCREMENT PRIMARY KEY,
    donor_id INTEGER NOT NULL REFERENCES donor(donor_id),
    entry_date DATETIME NOT NULL,
    plaid_transaction_id VARCHAR(255) NOT NULL,
    plaid_transaction_name VARCHAR(255) NOT NULL,
    plaid_transaction_city VARCHAR(255),
    plaid_transaction_type VARCHAR(255) NOT NULL,
    plaid_transaction_date DATETIME NOT NULL,
    plaid_transaction_amt FLOAT NOT NULL,
    plaid_account_id VARCHAR(255) NOT NULL,
    plaid_account_owner VARCHAR(255),
    donation_amt FLOAT NOT NULL
);

-- CREATE TABLE IF NOT EXISTS plaid_Setup (
--     donor_id INTEGER REFERENCES donor(donor_id),
--     entry_date DATETIME NOT NULL,
--     plaid_access_token VARCHAR(255) NOT NULL,
--     status BOOLEAN NOT NULL
-- );

CREATE TABLE IF NOT EXISTS donation (
    donation_id INTEGER AUTO_INCREMENT PRIMARY KEY,
    donor_id INTEGER REFERENCES donor(donor_id),
    drive_id INTEGER REFERENCES donor(drive_id),
    charity_id INTEGER REFERENCES charity(char_id),
    donation_date DATETIME NOT NULL,
    donation_amt FLOAT NOT NULL,
    donation_type VARCHAR(3) NOT NULL
);



-- Insert Statements -------------------------------------------------------------------
Insert into charity (
  char_name,  char_desc, char_image,
  char_address, char_city, char_state,
  activation_date,
  last_logged_in,
  charity_login,
  password,
  active_drives,
  causes,
  charity_type,
  charity_nav_score,
  tax_deductible
)
values (
  "The Pollination Project Foundation",
  "The Pollination Project is a foundation that makes seed grants, 365 days a year, to individual social change agents who seek to spread compassion in their communities and in the world for the benefit of all.",
  "https://cdn.greatnonprofits.org/images/logos/Logo_Square_ORANGE0.jpg",
  "15 Berkeley Way, Berkeley","Berkeley", "CA",
  SYSDATE(), SYSDATE(),
  "charity1","charity1",
  5,"Community Foundations, Philanthropy, Charity & Voluntarism Promotion, Voluntarism \& Grantmaking Foundations",
  "Charity Nav Type",0.0,True

),(
  "The Ama Foundation",
  "The Ama Foundation was created to provide a home, family environment and education for the most underprivileged children of Nepal.  we rescue children from trafficking, drugs and malnutrition and help them to grow up to be productive, happy and healthy citizens of Nepal",
  "https://cdn.greatnonprofits.org/images/logos/AmaLogoDarkRedWords.jpg",
  "25 Berkeley Way, Berkeley","Berkeley", "CA",
  SYSDATE(), SYSDATE(),
  "charity2","charity2",
  3,"Children & Youth, Education, Homeless & Housing, International Relief",
  "Charity Nav Type",6.4,True
),
(
  "Chaparral Foundation",
  "Chaparral House provides care for frail elders in a dynamic, life-affirming, homelike environment where privacy and self-esteem are respected, freedom of choice and freedom of expression are encouraged, and participation and contribution are appreciated.",
  "https://cdn.greatnonprofits.org/images/logos/CHAPARRAL_LOGO_JPG_small72.jpg",
  "35 Berkeley Way, Berkeley","Berkeley", "CA",
  SYSDATE(), SYSDATE(),
  "charity3","charity3",
  2,"Health, Nursing Facilities, Philanthropy, Private Operating Foundations, Seniors",
  "Charity Nav Type",7.5,False
);








Insert into drive (
charity_id
,name
,drive_desc
,drive_image
,target_amt
,collected_amt
,begin_date
,end_date
,active_status,
drive_city,
drive_state
,causes
,activation_date
,is_default)

values (
1,"Save the pollens - Non deafult",
"The Pollination Project is a foundation that makes seed grants, 365 days a year, to individual social change agents who seek to spread compassion in their communities and in the world for the benefit of all.",
"https://cdn.greatnonprofits.org/images/logos/Logo_Square_ORANGE0.jpg",
600.00,10.00,SYSDATE(),NULL,True,
"Berkeley","CA","Community Foundations, Nature", SYSDATE(),False
),
(
1,"Support Unlocking Silent",
"Support Unlocking Silent Histories in its startup phase and later with an impact grant. With the support of TPP, we have been able to many Indigenous youth both providing them with leadership jobs and inspiring young people to tell their stories from their perspectives",
"https://greatnonprofits.org/images/uploads/reviews/ush.jpg",
5000.00,2000.00,SYSDATE(),NULL,True,
"Berkeley","CA","Charity & Voluntarism Promotion", SYSDATE(),False
),
(
3,"Renovating Chaparral House",
"The Pollination Project is a foundation that makes seed grants, 365 days a year, to individual social change agents who seek to spread compassion in their communities and in the world for the benefit of all.",
"https://cdn.greatnonprofits.org/images/logos/CHAPARRAL_LOGO_JPG_small72.jpg",
200.00,90.00,SYSDATE(),NULL,True,
"Berkeley","CA","Health, Nursing Facilities, Seniors", SYSDATE(),True
)
;
