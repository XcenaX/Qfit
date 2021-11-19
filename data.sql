--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.10
-- Dumped by pg_dump version 9.6.10

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: _adminpanel_adminuser; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._adminpanel_adminuser (
    id smallint,
    username character varying(300) DEFAULT NULL::character varying,
    password integer,
    company_id smallint
);


ALTER TABLE public._adminpanel_adminuser OWNER TO rebasedata;

--
-- Name: _api_company; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._api_company (
    id smallint,
    name character varying(300) DEFAULT NULL::character varying,
    address character varying(300) DEFAULT NULL::character varying,
    latitude numeric(8,6) DEFAULT NULL::numeric,
    longitude numeric(8,6) DEFAULT NULL::numeric,
    owner_id smallint,
    qr_url character varying(300) DEFAULT NULL::character varying,
    all_bonuses smallint,
    avatar character varying(300) DEFAULT NULL::character varying,
    count_people smallint,
    contacts character varying(300) DEFAULT NULL::character varying,
    rating smallint,
    description character varying(300) DEFAULT NULL::character varying
);


ALTER TABLE public._api_company OWNER TO rebasedata;

--
-- Name: _api_company_days; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._api_company_days (
    id smallint,
    company_id smallint,
    schedule_id smallint
);


ALTER TABLE public._api_company_days OWNER TO rebasedata;

--
-- Name: _api_company_images; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._api_company_images (
    id smallint,
    company_id smallint,
    myimage_id smallint
);


ALTER TABLE public._api_company_images OWNER TO rebasedata;

--
-- Name: _api_company_tags; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._api_company_tags (
    id smallint,
    company_id smallint,
    servicecategory_id smallint
);


ALTER TABLE public._api_company_tags OWNER TO rebasedata;

--
-- Name: _api_finishedtrain; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._api_finishedtrain (
    id smallint,
    minutes smallint,
    start_time character varying(300) DEFAULT NULL::character varying,
    end_time character varying(300) DEFAULT NULL::character varying,
    bill smallint,
    company_id smallint,
    user_id smallint
);


ALTER TABLE public._api_finishedtrain OWNER TO rebasedata;

--
-- Name: _api_myimage; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._api_myimage (
    id smallint,
    image character varying(300) DEFAULT NULL::character varying
);


ALTER TABLE public._api_myimage OWNER TO rebasedata;

--
-- Name: _api_role; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._api_role (
    id smallint,
    name character varying(300) DEFAULT NULL::character varying
);


ALTER TABLE public._api_role OWNER TO rebasedata;

--
-- Name: _api_schedule; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._api_schedule (
    id smallint,
    day smallint
);


ALTER TABLE public._api_schedule OWNER TO rebasedata;

--
-- Name: _api_schedule_timelines; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._api_schedule_timelines (
    id smallint,
    schedule_id smallint,
    timeline_id smallint
);


ALTER TABLE public._api_schedule_timelines OWNER TO rebasedata;

--
-- Name: _api_servicecategory; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._api_servicecategory (
    id smallint,
    name character varying(300) DEFAULT NULL::character varying,
    image character varying(300) DEFAULT NULL::character varying
);


ALTER TABLE public._api_servicecategory OWNER TO rebasedata;

--
-- Name: _api_timeline; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._api_timeline (
    id smallint,
    start_time character varying(300) DEFAULT NULL::character varying,
    end_time character varying(300) DEFAULT NULL::character varying,
    price smallint,
    company_id smallint,
    day smallint
);


ALTER TABLE public._api_timeline OWNER TO rebasedata;

--
-- Name: _api_timer; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._api_timer (
    id smallint,
    start_time character varying(300) DEFAULT NULL::character varying,
    end_time character varying(300) DEFAULT NULL::character varying,
    company_id smallint,
    user_id smallint,
    day character varying(300) DEFAULT NULL::character varying,
    is_paid smallint
);


ALTER TABLE public._api_timer OWNER TO rebasedata;

--
-- Name: _api_traintimer; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._api_traintimer (
    id character varying(300) DEFAULT NULL::character varying,
    end_time character varying(300) DEFAULT NULL::character varying,
    company_id character varying(300) DEFAULT NULL::character varying,
    user_id character varying(300) DEFAULT NULL::character varying,
    start_time character varying(300) DEFAULT NULL::character varying
);


ALTER TABLE public._api_traintimer OWNER TO rebasedata;

--
-- Name: _api_user; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._api_user (
    id smallint,
    phone character varying(300) DEFAULT NULL::character varying,
    role_id smallint,
    avatar character varying(300) DEFAULT NULL::character varying,
    ref_code character varying(300) DEFAULT NULL::character varying,
    bonuses smallint,
    email character varying(300) DEFAULT NULL::character varying,
    name character varying(300) DEFAULT NULL::character varying,
    sex character varying(300) DEFAULT NULL::character varying,
    month_bonuses integer
);


ALTER TABLE public._api_user OWNER TO rebasedata;

--
-- Name: _api_user_friends; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._api_user_friends (
    id smallint,
    from_user_id smallint,
    to_user_id smallint
);


ALTER TABLE public._api_user_friends OWNER TO rebasedata;

--
-- Name: _api_verificationphone; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._api_verificationphone (
    id character varying(300) DEFAULT NULL::character varying,
    phone character varying(300) DEFAULT NULL::character varying,
    code character varying(300) DEFAULT NULL::character varying
);


ALTER TABLE public._api_verificationphone OWNER TO rebasedata;

--
-- Name: _auth_group; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._auth_group (
    id character varying(300) DEFAULT NULL::character varying,
    name character varying(300) DEFAULT NULL::character varying
);


ALTER TABLE public._auth_group OWNER TO rebasedata;

--
-- Name: _auth_group_permissions; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._auth_group_permissions (
    id character varying(300) DEFAULT NULL::character varying,
    group_id character varying(300) DEFAULT NULL::character varying,
    permission_id character varying(300) DEFAULT NULL::character varying
);


ALTER TABLE public._auth_group_permissions OWNER TO rebasedata;

--
-- Name: _auth_permission; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._auth_permission (
    id smallint,
    content_type_id smallint,
    codename character varying(300) DEFAULT NULL::character varying,
    name character varying(300) DEFAULT NULL::character varying
);


ALTER TABLE public._auth_permission OWNER TO rebasedata;

--
-- Name: _auth_user; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._auth_user (
    id smallint,
    password character varying(300) DEFAULT NULL::character varying,
    last_login character varying(300) DEFAULT NULL::character varying,
    is_superuser smallint,
    username character varying(300) DEFAULT NULL::character varying,
    last_name character varying(300) DEFAULT NULL::character varying,
    email character varying(300) DEFAULT NULL::character varying,
    is_staff smallint,
    is_active smallint,
    date_joined character varying(300) DEFAULT NULL::character varying,
    first_name character varying(300) DEFAULT NULL::character varying
);


ALTER TABLE public._auth_user OWNER TO rebasedata;

--
-- Name: _auth_user_groups; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._auth_user_groups (
    id character varying(300) DEFAULT NULL::character varying,
    user_id character varying(300) DEFAULT NULL::character varying,
    group_id character varying(300) DEFAULT NULL::character varying
);


ALTER TABLE public._auth_user_groups OWNER TO rebasedata;

--
-- Name: _auth_user_user_permissions; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._auth_user_user_permissions (
    id character varying(300) DEFAULT NULL::character varying,
    user_id character varying(300) DEFAULT NULL::character varying,
    permission_id character varying(300) DEFAULT NULL::character varying
);


ALTER TABLE public._auth_user_user_permissions OWNER TO rebasedata;

--
-- Name: _authtoken_token; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._authtoken_token (
    key character varying(300) DEFAULT NULL::character varying,
    created character varying(300) DEFAULT NULL::character varying,
    user_id smallint
);


ALTER TABLE public._authtoken_token OWNER TO rebasedata;

--
-- Name: _django_admin_log; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._django_admin_log (
    id smallint,
    action_time character varying(300) DEFAULT NULL::character varying,
    object_id smallint,
    object_repr character varying(300) DEFAULT NULL::character varying,
    change_message character varying(300) DEFAULT NULL::character varying,
    content_type_id smallint,
    user_id smallint,
    action_flag smallint
);


ALTER TABLE public._django_admin_log OWNER TO rebasedata;

--
-- Name: _django_content_type; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._django_content_type (
    id smallint,
    app_label character varying(300) DEFAULT NULL::character varying,
    model character varying(300) DEFAULT NULL::character varying
);


ALTER TABLE public._django_content_type OWNER TO rebasedata;

--
-- Name: _django_migrations; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._django_migrations (
    id smallint,
    app character varying(300) DEFAULT NULL::character varying,
    name character varying(300) DEFAULT NULL::character varying,
    applied character varying(300) DEFAULT NULL::character varying
);


ALTER TABLE public._django_migrations OWNER TO rebasedata;

--
-- Name: _django_session; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._django_session (
    session_key character varying(300) DEFAULT NULL::character varying,
    session_data character varying(300) DEFAULT NULL::character varying,
    expire_date character varying(300) DEFAULT NULL::character varying
);


ALTER TABLE public._django_session OWNER TO rebasedata;

--
-- Name: _sqlite_sequence; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._sqlite_sequence (
    name character varying(300) DEFAULT NULL::character varying,
    seq smallint
);


ALTER TABLE public._sqlite_sequence OWNER TO rebasedata;

--
-- Data for Name: _adminpanel_adminuser; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._adminpanel_adminuser (id, username, password, company_id) FROM stdin;
5	XcenaX	12345	5
\.


--
-- Data for Name: _api_company; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._api_company (id, name, address, latitude, longitude, owner_id, qr_url, all_bonuses, avatar, count_people, contacts, rating, description) FROM stdin;
5	Futness Club	Сатпаева 25	51.128262	71.430486	5	https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=5	0	clubs_avatars/36501350415.png	100	+77011242693	5	Хороший клуб 2
\.


--
-- Data for Name: _api_company_days; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._api_company_days (id, company_id, schedule_id) FROM stdin;
6	5	190
7	5	191
1	5	192
2	5	193
3	5	194
4	5	195
5	5	196
\.


--
-- Data for Name: _api_company_images; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._api_company_images (id, company_id, myimage_id) FROM stdin;
3	5	29
5	5	31
\.


--
-- Data for Name: _api_company_tags; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._api_company_tags (id, company_id, servicecategory_id) FROM stdin;
15	5	1
16	5	2
14	5	3
\.


--
-- Data for Name: _api_finishedtrain; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._api_finishedtrain (id, minutes, start_time, end_time, bill, company_id, user_id) FROM stdin;
36	60			1500	5	5
\.


--
-- Data for Name: _api_myimage; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._api_myimage (id, image) FROM stdin;
2	services/logo.png
15	services/бог_nvzsWIZ.jpg
16	services/БОГИ_bWIugkE.jpg
17	services/бог_aTAoIWh.jpg
19	services/БОГИ_p2BF5Uv.jpg
21	services/бог_lj1XrbN.png
24	services/бог.png
26	services/logo.png
29	club_images/30258560055418376_790a_600x600.png
31	club_images/2912-medium_YVmcEJI.png
\.


--
-- Data for Name: _api_role; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._api_role (id, name) FROM stdin;
1	user
2	company
3	admin
\.


--
-- Data for Name: _api_schedule; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._api_schedule (id, day) FROM stdin;
190	0
191	1
192	2
193	3
194	4
195	5
196	6
\.


--
-- Data for Name: _api_schedule_timelines; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._api_schedule_timelines (id, schedule_id, timeline_id) FROM stdin;
49	190	49
50	191	50
\.


--
-- Data for Name: _api_servicecategory; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._api_servicecategory (id, name, image) FROM stdin;
1	Бассейн	services_categories/interior-of-fitness-hall-with-fitness-bicycles-WN97KUY_1_1.png
2	Боевые искусства	services_categories/бокс.png
3	Тренажерный зал	services_categories/interior-of-fitness-hall-with-fitness-bicycles-WN97KUY_1.png
4	Йога	
5	Танцы	
6	Сауна	
\.


--
-- Data for Name: _api_timeline; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._api_timeline (id, start_time, end_time, price, company_id, day) FROM stdin;
49	10:00:00	14:00:00	25	5	0
50	10:00:00	14:00:00	25	5	1
\.


--
-- Data for Name: _api_timer; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._api_timer (id, start_time, end_time, company_id, user_id, day, is_paid) FROM stdin;
1	10:00:00	14:00:00	5	5		0
\.


--
-- Data for Name: _api_traintimer; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._api_traintimer (id, end_time, company_id, user_id, start_time) FROM stdin;
\.


--
-- Data for Name: _api_user; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._api_user (id, phone, role_id, avatar, ref_code, bonuses, email, name, sex, month_bonuses) FROM stdin;
5	+77011242693	1	avatars/ава.png	1ILL3K9X	0	a	a	a	10000
7	+77021242693	1			0	a	a	a	5000
\.


--
-- Data for Name: _api_user_friends; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._api_user_friends (id, from_user_id, to_user_id) FROM stdin;
1	5	7
2	7	5
\.


--
-- Data for Name: _api_verificationphone; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._api_verificationphone (id, phone, code) FROM stdin;
\.


--
-- Data for Name: _auth_group; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: _auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: _auth_permission; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._auth_permission (id, content_type_id, codename, name) FROM stdin;
1	1	add_role	Can add role
2	1	change_role	Can change role
3	1	delete_role	Can delete role
4	1	view_role	Can view role
5	2	add_user	Can add user
6	2	change_user	Can change user
7	2	delete_user	Can delete user
8	2	view_user	Can view user
9	3	add_company	Can add company
10	3	change_company	Can change company
11	3	delete_company	Can delete company
12	3	view_company	Can view company
13	4	add_logentry	Can add log entry
14	4	change_logentry	Can change log entry
15	4	delete_logentry	Can delete log entry
16	4	view_logentry	Can view log entry
17	5	add_permission	Can add permission
18	5	change_permission	Can change permission
19	5	delete_permission	Can delete permission
20	5	view_permission	Can view permission
21	6	add_group	Can add group
22	6	change_group	Can change group
23	6	delete_group	Can delete group
24	6	view_group	Can view group
25	7	add_user	Can add user
26	7	change_user	Can change user
27	7	delete_user	Can delete user
28	7	view_user	Can view user
29	8	add_contenttype	Can add content type
30	8	change_contenttype	Can change content type
31	8	delete_contenttype	Can delete content type
32	8	view_contenttype	Can view content type
33	9	add_session	Can add session
34	9	change_session	Can change session
35	9	delete_session	Can delete session
36	9	view_session	Can view session
37	10	add_schedule	Can add schedule
38	10	change_schedule	Can change schedule
39	10	delete_schedule	Can delete schedule
40	10	view_schedule	Can view schedule
41	11	add_traintimer	Can add train timer
42	11	change_traintimer	Can change train timer
43	11	delete_traintimer	Can delete train timer
44	11	view_traintimer	Can view train timer
45	12	add_timer	Can add timer
46	12	change_timer	Can change timer
47	12	delete_timer	Can delete timer
48	12	view_timer	Can view timer
49	13	add_service	Can add service
50	13	change_service	Can change service
51	13	delete_service	Can delete service
52	13	view_service	Can view service
53	14	add_finishedtrains	Can add finished trains
54	14	change_finishedtrains	Can change finished trains
55	14	delete_finishedtrains	Can delete finished trains
56	14	view_finishedtrains	Can view finished trains
57	14	add_finishedtrain	Can add finished train
58	14	change_finishedtrain	Can change finished train
59	14	delete_finishedtrain	Can delete finished train
60	14	view_finishedtrain	Can view finished train
61	15	add_myimage	Can add my image
62	15	change_myimage	Can change my image
63	15	delete_myimage	Can delete my image
64	15	view_myimage	Can view my image
65	16	add_adminuser	Can add admin user
66	16	change_adminuser	Can change admin user
67	16	delete_adminuser	Can delete admin user
68	16	view_adminuser	Can view admin user
69	17	add_adminuser	Can add admin user
70	17	change_adminuser	Can change admin user
71	17	delete_adminuser	Can delete admin user
72	17	view_adminuser	Can view admin user
73	18	add_timeline	Can add time line
74	18	change_timeline	Can change time line
75	18	delete_timeline	Can delete time line
76	18	view_timeline	Can view time line
77	19	add_token	Can add Token
78	19	change_token	Can change Token
79	19	delete_token	Can delete Token
80	19	view_token	Can view Token
81	20	add_tokenproxy	Can add token
82	20	change_tokenproxy	Can change token
83	20	delete_tokenproxy	Can delete token
84	20	view_tokenproxy	Can view token
85	21	add_servicecategory	Can add service category
86	21	change_servicecategory	Can change service category
87	21	delete_servicecategory	Can delete service category
88	21	view_servicecategory	Can view service category
89	22	add_verificationphone	Can add verification phone
90	22	change_verificationphone	Can change verification phone
91	22	delete_verificationphone	Can delete verification phone
92	22	view_verificationphone	Can view verification phone
\.


--
-- Data for Name: _auth_user; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._auth_user (id, password, last_login, is_superuser, username, last_name, email, is_staff, is_active, date_joined, first_name) FROM stdin;
6	pbkdf2_sha256$216000$k8A7dOENfoWb$CmVFZvD9DFH14HdyWVCEAlxRZHni/JOSjqP7SQFkHxE=	2021-04-20	1	XcenaX		vlad-057@mail.ru	1	1	2021-03-16	
\.


--
-- Data for Name: _auth_user_groups; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: _auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: _authtoken_token; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._authtoken_token (key, created, user_id) FROM stdin;
7f47614dda172a6a6201a9b3a2869a0a63110a88	2021-03-19	6
\.


--
-- Data for Name: _django_admin_log; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._django_admin_log (id, action_time, object_id, object_repr, change_message, content_type_id, user_id, action_flag) FROM stdin;
92	2021-03-18	2	XcenaX	[{"added": {}}]	16	6	1
93	2021-03-29	32	87011242693		14	6	3
94	2021-03-29	31	87011242693		14	6	3
95	2021-03-29	30	87011242693		14	6	3
96	2021-03-29	29	87011242693		14	6	3
97	2021-03-29	28	87011242693		14	6	3
98	2021-03-29	27	87011242693		14	6	3
99	2021-03-29	26	87011242693		14	6	3
100	2021-03-29	25	87011242693		14	6	3
101	2021-03-29	24	87011242693		14	6	3
102	2021-03-29	2	(87011242693) Fitness Club: 2021-03-29 21:40:00		12	6	3
103	2021-03-29	1	(87011242693) Fitness Club: 2021-03-29 20:40:00		12	6	3
104	2021-03-31	5	(87011242693) Fitness Club: 2021-03-30 15:20:00		12	6	3
105	2021-03-31	4	(87011242693) Fitness Club: 2021-03-30 15:20:00		12	6	3
106	2021-03-31	6	(87011242693) Fitness Club: 2021-03-30 15:20:00		12	6	3
107	2021-04-05	7	87021242693	[{"added": {}}]	2	6	1
108	2021-04-05	5	87011242693	[{"changed": {"fields": ["Friends"]}}]	2	6	2
109	2021-04-06	3	XcenaX2	[{"added": {}}]	16	6	1
110	2021-04-06	10	Wninex		3	6	3
111	2021-04-06	9	esfoiweoif		3	6	3
112	2021-04-06	8	esfoiweoif		3	6	3
113	2021-04-06	7	esfoiweoif		3	6	3
114	2021-04-06	4	XcenaX2	[{"added": {}}]	16	6	1
115	2021-04-11	5	87011242693	[{"changed": {"fields": ["Month bonuses", "Email", "Name", "Sex"]}}]	2	6	2
116	2021-04-11	7	87021242693	[{"changed": {"fields": ["Month bonuses", "Friends", "Email", "Name", "Sex"]}}]	2	6	2
117	2021-04-11	6	Winex		3	6	3
118	2021-04-11	5	Fitness Club		3	6	3
119	2021-04-11	1	Fitness Club	[{"added": {}}]	3	6	1
120	2021-04-11	1	Fitness Club		3	6	3
121	2021-04-11	2	Fitnness	[{"added": {}}]	3	6	1
122	2021-04-11	189	Воскресенье		10	6	3
123	2021-04-11	188	Суббота		10	6	3
124	2021-04-11	187	Пятница		10	6	3
125	2021-04-11	186	Четверг		10	6	3
126	2021-04-11	185	Среда		10	6	3
127	2021-04-11	184	Вторник		10	6	3
128	2021-04-11	183	Понедельник		10	6	3
129	2021-04-11	182	Воскресенье		10	6	3
130	2021-04-11	181	Суббота		10	6	3
131	2021-04-11	180	Пятница		10	6	3
132	2021-04-11	179	Четверг		10	6	3
133	2021-04-11	178	Среда		10	6	3
134	2021-04-11	177	Вторник		10	6	3
135	2021-04-11	176	Понедельник		10	6	3
136	2021-04-11	175	Воскресенье		10	6	3
137	2021-04-11	174	Суббота		10	6	3
138	2021-04-11	173	Пятница		10	6	3
139	2021-04-11	172	Четверг		10	6	3
140	2021-04-11	171	Среда		10	6	3
141	2021-04-11	170	Вторник		10	6	3
142	2021-04-11	169	Понедельник		10	6	3
143	2021-04-11	168	Воскресенье		10	6	3
144	2021-04-11	167	Суббота		10	6	3
145	2021-04-11	166	Пятница		10	6	3
146	2021-04-11	165	Четверг		10	6	3
147	2021-04-11	164	Среда		10	6	3
148	2021-04-11	163	Вторник		10	6	3
149	2021-04-11	162	Понедельник		10	6	3
150	2021-04-11	161	Воскресенье		10	6	3
151	2021-04-11	160	Суббота		10	6	3
152	2021-04-11	159	Пятница		10	6	3
153	2021-04-11	158	Четверг		10	6	3
154	2021-04-11	157	Среда		10	6	3
155	2021-04-11	156	Вторник		10	6	3
156	2021-04-11	155	Понедельник		10	6	3
157	2021-04-11	154	Воскресенье		10	6	3
158	2021-04-11	153	Суббота		10	6	3
159	2021-04-11	152	Пятница		10	6	3
160	2021-04-11	151	Четверг		10	6	3
161	2021-04-11	150	Среда		10	6	3
162	2021-04-11	149	Вторник		10	6	3
163	2021-04-11	148	Понедельник		10	6	3
164	2021-04-11	147	Воскресенье		10	6	3
165	2021-04-11	146	Суббота		10	6	3
166	2021-04-11	145	Пятница		10	6	3
167	2021-04-11	144	Четверг		10	6	3
168	2021-04-11	143	Среда		10	6	3
169	2021-04-11	142	Вторник		10	6	3
170	2021-04-11	141	Понедельник		10	6	3
171	2021-04-11	140	Воскресенье		10	6	3
172	2021-04-11	139	Суббота		10	6	3
173	2021-04-11	138	Пятница		10	6	3
174	2021-04-11	137	Четверг		10	6	3
175	2021-04-11	136	Среда		10	6	3
176	2021-04-11	135	Вторник		10	6	3
177	2021-04-11	134	Понедельник		10	6	3
178	2021-04-11	133	Воскресенье		10	6	3
179	2021-04-11	132	Суббота		10	6	3
180	2021-04-11	131	Пятница		10	6	3
181	2021-04-11	130	Четверг		10	6	3
182	2021-04-11	129	Среда		10	6	3
183	2021-04-11	128	Вторник		10	6	3
184	2021-04-11	127	Понедельник		10	6	3
185	2021-04-11	126	Воскресенье		10	6	3
186	2021-04-11	125	Суббота		10	6	3
187	2021-04-11	124	Пятница		10	6	3
188	2021-04-11	123	Четверг		10	6	3
189	2021-04-11	122	Среда		10	6	3
190	2021-04-11	121	Вторник		10	6	3
191	2021-04-11	120	Понедельник		10	6	3
192	2021-04-11	119	Воскресенье		10	6	3
193	2021-04-11	118	Суббота		10	6	3
194	2021-04-11	117	Пятница		10	6	3
195	2021-04-11	116	Четверг		10	6	3
196	2021-04-11	115	Среда		10	6	3
197	2021-04-11	114	Вторник		10	6	3
198	2021-04-11	113	Понедельник		10	6	3
199	2021-04-11	112	Воскресенье		10	6	3
200	2021-04-11	111	Суббота		10	6	3
201	2021-04-11	110	Пятница		10	6	3
202	2021-04-11	109	Четверг		10	6	3
203	2021-04-11	108	Среда		10	6	3
204	2021-04-11	107	Вторник		10	6	3
205	2021-04-11	106	Понедельник		10	6	3
206	2021-04-11	105	Воскресенье		10	6	3
207	2021-04-11	104	Суббота		10	6	3
208	2021-04-11	103	Пятница		10	6	3
209	2021-04-11	102	Четверг		10	6	3
210	2021-04-11	101	Среда		10	6	3
211	2021-04-11	100	Вторник		10	6	3
212	2021-04-11	99	Понедельник		10	6	3
213	2021-04-11	98	Воскресенье		10	6	3
214	2021-04-11	97	Суббота		10	6	3
215	2021-04-11	96	Пятница		10	6	3
216	2021-04-11	95	Четверг		10	6	3
217	2021-04-11	94	Среда		10	6	3
218	2021-04-11	93	Вторник		10	6	3
219	2021-04-11	92	Понедельник		10	6	3
220	2021-04-11	91	Воскресенье		10	6	3
221	2021-04-11	90	Суббота		10	6	3
222	2021-04-11	89	Пятница		10	6	3
223	2021-04-11	88	Четверг		10	6	3
224	2021-04-11	87	Среда		10	6	3
225	2021-04-11	86	Вторник		10	6	3
226	2021-04-11	85	Понедельник		10	6	3
227	2021-04-11	84	Воскресенье		10	6	3
228	2021-04-11	83	Суббота		10	6	3
229	2021-04-11	82	Пятница		10	6	3
230	2021-04-11	81	Четверг		10	6	3
231	2021-04-11	80	Среда		10	6	3
232	2021-04-11	79	Вторник		10	6	3
233	2021-04-11	78	Понедельник		10	6	3
234	2021-04-11	77	Воскресенье		10	6	3
235	2021-04-11	76	Суббота		10	6	3
236	2021-04-11	75	Пятница		10	6	3
237	2021-04-11	74	Четверг		10	6	3
238	2021-04-11	73	Среда		10	6	3
239	2021-04-11	72	Вторник		10	6	3
240	2021-04-11	71	Понедельник		10	6	3
241	2021-04-11	70	Воскресенье		10	6	3
242	2021-04-11	69	Суббота		10	6	3
243	2021-04-11	68	Пятница		10	6	3
244	2021-04-11	67	Четверг		10	6	3
245	2021-04-11	66	Среда		10	6	3
246	2021-04-11	65	Вторник		10	6	3
247	2021-04-11	64	Понедельник		10	6	3
248	2021-04-11	63	Воскресенье		10	6	3
249	2021-04-11	62	Суббота		10	6	3
250	2021-04-11	61	Пятница		10	6	3
251	2021-04-11	60	Четверг		10	6	3
252	2021-04-11	59	Среда		10	6	3
253	2021-04-11	58	Вторник		10	6	3
254	2021-04-11	57	Понедельник		10	6	3
255	2021-04-11	56	Воскресенье		10	6	3
256	2021-04-11	55	Суббота		10	6	3
257	2021-04-11	54	Пятница		10	6	3
258	2021-04-11	53	Четверг		10	6	3
259	2021-04-11	52	Среда		10	6	3
260	2021-04-11	51	Вторник		10	6	3
261	2021-04-11	50	Понедельник		10	6	3
262	2021-04-11	49	Воскресенье		10	6	3
263	2021-04-11	48	Суббота		10	6	3
264	2021-04-11	47	Пятница		10	6	3
265	2021-04-11	46	Четверг		10	6	3
266	2021-04-11	45	Среда		10	6	3
267	2021-04-11	44	Вторник		10	6	3
268	2021-04-11	43	Понедельник		10	6	3
269	2021-04-11	42	Воскресенье		10	6	3
270	2021-04-11	41	Суббота		10	6	3
271	2021-04-11	40	Пятница		10	6	3
272	2021-04-11	39	Четверг		10	6	3
273	2021-04-11	38	Среда		10	6	3
274	2021-04-11	37	Вторник		10	6	3
275	2021-04-11	36	Понедельник		10	6	3
276	2021-04-11	35	Воскресенье		10	6	3
277	2021-04-11	34	Суббота		10	6	3
278	2021-04-11	33	Пятница		10	6	3
279	2021-04-11	32	Четверг		10	6	3
280	2021-04-11	31	Среда		10	6	3
281	2021-04-11	30	Вторник		10	6	3
282	2021-04-11	29	Понедельник		10	6	3
283	2021-04-11	28	Воскресенье		10	6	3
284	2021-04-11	27	Суббота		10	6	3
285	2021-04-11	26	Пятница		10	6	3
286	2021-04-11	25	Четверг		10	6	3
287	2021-04-11	24	Среда		10	6	3
288	2021-04-11	23	Вторник		10	6	3
289	2021-04-11	22	Понедельник		10	6	3
290	2021-04-11	21	Воскресенье		10	6	3
291	2021-04-11	20	Суббота		10	6	3
292	2021-04-11	19	Пятница		10	6	3
293	2021-04-11	18	Четверг		10	6	3
294	2021-04-11	17	Среда		10	6	3
295	2021-04-11	16	Вторник		10	6	3
296	2021-04-11	15	Понедельник		10	6	3
297	2021-04-11	14	Воскресенье		10	6	3
298	2021-04-11	13	Суббота		10	6	3
299	2021-04-11	12	Пятница		10	6	3
300	2021-04-11	11	Четверг		10	6	3
301	2021-04-11	10	Среда		10	6	3
302	2021-04-11	9	Вторник		10	6	3
303	2021-04-11	8	Понедельник		10	6	3
304	2021-04-11	7	Пятница		10	6	3
305	2021-04-11	6	Вторник		10	6	3
306	2021-04-11	5	Воскресенье		10	6	3
307	2021-04-11	4	Суббота		10	6	3
308	2021-04-11	3	Четверг		10	6	3
309	2021-04-11	2	Среда		10	6	3
310	2021-04-11	1	Понедельник		10	6	3
311	2021-04-11	2	Fitnness		3	6	3
312	2021-04-11	3	ufhiwuefwehf	[{"added": {}}]	3	6	1
313	2021-04-11	3	ufhiwuefwehf		3	6	3
314	2021-04-11	4	wef wfwwffwefwe	[{"added": {}}]	3	6	1
315	2021-04-11	4	wef wfwwffwefwe		3	6	3
316	2021-04-12	7	+77021242693	[{"changed": {"fields": ["Phone"]}}]	2	6	2
317	2021-04-12	5	+77011242693	[{"changed": {"fields": ["Phone"]}}]	2	6	2
318	2021-04-12	5	XcenaX	[{"added": {}}]	16	6	1
319	2021-04-12	43	TimeLine object (43)		18	6	3
320	2021-04-12	41	TimeLine object (41)		18	6	3
321	2021-04-12	38	TimeLine object (38)		18	6	3
322	2021-04-12	37	TimeLine object (37)		18	6	3
323	2021-04-12	35	TimeLine object (35)		18	6	3
324	2021-04-12	33	TimeLine object (33)		18	6	3
325	2021-04-12	31	TimeLine object (31)		18	6	3
326	2021-04-12	30	TimeLine object (30)		18	6	3
327	2021-04-12	29	TimeLine object (29)		18	6	3
328	2021-04-12	28	TimeLine object (28)		18	6	3
329	2021-04-12	27	TimeLine object (27)		18	6	3
330	2021-04-12	15	TimeLine object (15)		18	6	3
331	2021-04-12	14	TimeLine object (14)		18	6	3
332	2021-04-12	13	TimeLine object (13)		18	6	3
333	2021-04-12	12	TimeLine object (12)		18	6	3
334	2021-04-12	11	TimeLine object (11)		18	6	3
335	2021-04-12	10	TimeLine object (10)		18	6	3
336	2021-04-12	9	TimeLine object (9)		18	6	3
337	2021-04-12	1	TimeLine object (1)		18	6	3
338	2021-04-12	45	TimeLine object (45)	[{"changed": {"fields": ["Day"]}}]	18	6	2
339	2021-04-12	5	Futness Club	[{"changed": {"fields": ["Count people"]}}]	3	6	2
340	2021-04-13	48	TimeLine object (48)		18	6	3
341	2021-04-13	46	TimeLine object (46)		18	6	3
342	2021-04-13	45	TimeLine object (45)		18	6	3
343	2021-04-13	3	(+77011242693) Futness Club: 14:00:00	[{"changed": {"fields": ["Is confirmed"]}}]	12	6	2
344	2021-04-13	5	Futness Club	[{"changed": {"fields": ["Tags"]}}]	3	6	2
345	2021-04-13	3	Качалка	[{"changed": {"fields": ["Image"]}}]	21	6	2
346	2021-04-13	2	Бокс	[{"changed": {"fields": ["Image"]}}]	21	6	2
347	2021-04-13	1	Бассейн	[{"changed": {"fields": ["Image"]}}]	21	6	2
348	2021-04-14	4	(+77011242693) : 14:00:00	[{"added": {}}]	12	6	1
349	2021-04-18	8	87011242693	[{"added": {}}]	2	6	1
350	2021-04-18	8	87011242693		2	6	3
351	2021-04-20	3	Тренажерный зал	[{"changed": {"fields": ["Name"]}}]	21	6	2
352	2021-04-20	6	A2Fitness	[{"added": {}}]	3	6	1
353	2021-04-20	7	FirWorx	[{"added": {}}]	3	6	1
354	2021-04-20	8	Sanat Fit	[{"added": {}}]	3	6	1
355	2021-04-20	9	Алау фитнесс	[{"added": {}}]	3	6	1
356	2021-04-20	10	Grand Fitness	[{"added": {}}]	3	6	1
357	2021-04-20	11	Adam Fit	[{"added": {}}]	3	6	1
358	2021-04-20	12	World Class Green	[{"added": {}}]	3	6	1
359	2021-04-20	12	World Class Green	[{"changed": {"fields": ["Qr url"]}}]	3	6	2
360	2021-04-20	11	Adam Fit	[{"changed": {"fields": ["Qr url"]}}]	3	6	2
361	2021-04-20	10	Grand Fitness	[{"changed": {"fields": ["Qr url"]}}]	3	6	2
362	2021-04-20	9	Алау фитнесс	[{"changed": {"fields": ["Qr url"]}}]	3	6	2
363	2021-04-20	8	Sanat Fit	[{"changed": {"fields": ["Qr url"]}}]	3	6	2
364	2021-04-20	7	FirWorx	[{"changed": {"fields": ["Qr url"]}}]	3	6	2
365	2021-04-20	6	A2Fitness	[{"changed": {"fields": ["Qr url"]}}]	3	6	2
366	2021-04-20	2	Боевые искусства	[{"changed": {"fields": ["Name"]}}]	21	6	2
367	2021-04-20	4	Йога	[{"added": {}}]	21	6	1
368	2021-04-20	5	Танцы	[{"added": {}}]	21	6	1
369	2021-04-20	6	Сауна	[{"added": {}}]	21	6	1
370	2021-04-20	6	A2FIT	[{"added": {}}]	16	6	1
371	2021-04-20	7	FITWORX	[{"added": {}}]	16	6	1
372	2021-04-20	8	SANATFIT	[{"added": {}}]	16	6	1
373	2021-04-20	9	ALAYFIT	[{"added": {}}]	16	6	1
374	2021-04-20	10	GRANDFIT	[{"added": {}}]	16	6	1
375	2021-04-20	11	ADAMFIT	[{"added": {}}]	16	6	1
376	2021-04-20	12	WORLDCLASSGREEN	[{"added": {}}]	16	6	1
\.


--
-- Data for Name: _django_content_type; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._django_content_type (id, app_label, model) FROM stdin;
4	admin	logentry
16	adminpanel	adminuser
17	api	adminuser
3	api	company
14	api	finishedtrain
15	api	myimage
1	api	role
10	api	schedule
13	api	service
21	api	servicecategory
18	api	timeline
12	api	timer
11	api	traintimer
2	api	user
22	api	verificationphone
6	auth	group
5	auth	permission
7	auth	user
19	authtoken	token
20	authtoken	tokenproxy
8	contenttypes	contenttype
9	sessions	session
\.


--
-- Data for Name: _django_migrations; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2021-02-15
2	auth	0001_initial	2021-02-15
3	admin	0001_initial	2021-02-15
4	admin	0002_logentry_remove_auto_add	2021-02-15
5	admin	0003_logentry_add_action_flag_choices	2021-02-15
6	api	0001_initial	2021-02-15
7	contenttypes	0002_remove_content_type_name	2021-02-15
8	auth	0002_alter_permission_name_max_length	2021-02-15
9	auth	0003_alter_user_email_max_length	2021-02-15
10	auth	0004_alter_user_username_opts	2021-02-15
11	auth	0005_alter_user_last_login_null	2021-02-15
12	auth	0006_require_contenttypes_0002	2021-02-15
13	auth	0007_alter_validators_add_error_messages	2021-02-15
14	auth	0008_alter_user_username_max_length	2021-02-15
15	auth	0009_alter_user_last_name_max_length	2021-02-15
16	auth	0010_alter_group_name_max_length	2021-02-15
17	auth	0011_update_proxy_permissions	2021-02-15
18	auth	0012_alter_user_first_name_max_length	2021-02-15
19	sessions	0001_initial	2021-02-15
20	api	0002_auto_20210215_1944	2021-02-15
21	api	0003_auto_20210215_2008	2021-02-15
22	api	0004_auto_20210215_2011	2021-02-15
23	api	0005_auto_20210215_2015	2021-02-15
24	api	0006_auto_20210216_2229	2021-02-16
25	api	0007_auto_20210217_1510	2021-02-17
26	api	0008_auto_20210217_1512	2021-02-17
27	api	0009_auto_20210217_1642	2021-02-17
28	api	0010_auto_20210217_1650	2021-02-17
29	api	0011_auto_20210217_1734	2021-02-17
30	api	0012_auto_20210220_1443	2021-02-20
31	api	0013_auto_20210220_1451	2021-02-20
32	api	0014_auto_20210220_1454	2021-02-20
33	api	0015_auto_20210221_1630	2021-02-21
34	api	0016_auto_20210224_2103	2021-02-24
35	adminpanel	0001_initial	2021-02-24
36	adminpanel	0002_delete_adminuser	2021-02-25
37	api	0017_auto_20210225_1844	2021-02-25
38	api	0018_auto_20210225_2029	2021-02-25
39	adminpanel	0003_adminuser	2021-02-25
40	api	0019_auto_20210225_2032	2021-02-25
41	api	0020_auto_20210227_1514	2021-02-27
42	api	0021_auto_20210227_1522	2021-02-27
43	api	0022_auto_20210304_1231	2021-03-04
44	api	0023_auto_20210304_1232	2021-03-04
45	authtoken	0001_initial	2021-03-12
46	authtoken	0002_auto_20160226_1747	2021-03-12
47	authtoken	0003_tokenproxy	2021-03-12
48	api	0024_auto_20210312_1347	2021-03-12
49	api	0025_auto_20210317_1318	2021-03-17
50	api	0026_auto_20210317_1323	2021-03-17
51	api	0027_auto_20210319_1306	2021-03-19
52	api	0028_auto_20210320_1915	2021-03-20
53	api	0029_auto_20210325_1521	2021-03-25
54	api	0030_auto_20210325_1523	2021-03-25
55	api	0031_auto_20210329_1956	2021-03-29
56	api	0032_auto_20210331_1419	2021-03-31
57	api	0033_auto_20210405_1727	2021-04-05
58	api	0034_auto_20210405_1730	2021-04-05
59	api	0035_auto_20210406_1554	2021-04-06
60	api	0036_auto_20210406_1556	2021-04-06
61	api	0037_auto_20210406_1739	2021-04-06
62	api	0038_auto_20210406_1803	2021-04-06
63	api	0039_auto_20210410_1317	2021-04-10
64	api	0040_auto_20210411_1449	2021-04-11
65	api	0041_auto_20210411_1708	2021-04-11
66	api	0042_auto_20210411_1924	2021-04-11
67	api	0043_auto_20210411_1931	2021-04-11
68	api	0044_auto_20210411_1934	2021-04-11
69	api	0045_auto_20210411_1939	2021-04-11
70	api	0046_auto_20210411_1947	2021-04-11
71	api	0047_auto_20210411_1950	2021-04-11
72	api	0048_auto_20210412_1842	2021-04-12
73	api	0049_auto_20210412_1854	2021-04-12
74	api	0050_auto_20210412_2110	2021-04-12
75	api	0051_auto_20210413_1605	2021-04-13
76	api	0052_auto_20210414_1518	2021-04-14
77	api	0053_auto_20210418_1844	2021-04-18
78	api	0054_auto_20210418_1844	2021-04-18
79	api	0055_auto_20210419_0040	2021-04-19
80	api	0056_auto_20210419_0041	2021-04-19
81	api	0057_auto_20210419_0043	2021-04-19
82	api	0058_auto_20210419_0043	2021-04-19
83	api	0059_auto_20210420_1529	2021-04-20
\.


--
-- Data for Name: _django_session; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._django_session (session_key, session_data, expire_date) FROM stdin;
ywmmdwph3ectflin8187pkfhm9b3yw8y	.eJxVjDsOwyAQRO9CbSFgAWOX6XMGaxfWsfOByJ8iinL32JKLpBvNvHlv0eG6DN0689SNSbQCRPXbEcYb531IV8yXImPJyzSS3BF5rLM8l8T308H-CQach-2tNQTFBBYduWAMGNWQN30IBFrVoHwMUAd2jKlBm5zviVmTaZJ2zvpNGsvjifklWl2JXb2FzxeAXD16:1lGjza:nmJlmoIyhuDnSXgRtI3GDnMgjlyk7eWdtypiowZcamY	2021-03-15
4aue5dbigrzwq4h00narx15fhenhsfc3	.eJxVjjsOwyAQRO9CHSFgAWOX6XMGaxfWsfMBy58iinL32JIbt_NmnuYrYnmPmD-i0RfR4rr07Trz1A5JNALEKSOMT847SA_M9yJjycs0kNwr8qCzvJXEr-vRPQl6nPttrTUExQQWHblgDBhVkzddCARaVaB8DFAFdoypRpuc74hZk6mTds76Tbrrtsu_P37EPXo:1lHOpf:yd3NeUkoItSS7pu3mpuUG4SC4HiUhycK19LDRJOUBkU	2021-03-17
73nib3ridnoll7n9t39jxsv9yuwo50fh	.eJxVjDsOwjAQRO-yNbJsb-w4lPScIdq1NyR8bJRPgRB3h6A06Ubz3swblklGOJoDxPJ4Un79c0vL3LcraocER0DYdUzxJnkF6Ur5UlQseR4HVquiNjqpc0lyP23u7qCnqf-tjcGghbEixy5Yi1Y37G0XAqPRNWofA9ZBnFBqqErOdyxi2DbJOFd5-HwBTZU9eg:1lHrsQ:6vpVDMLv37izVw7pV-F4J8qexXtzot1_GWRfB8Z1Dxc	2021-03-18
o31wop4szabjdkcnvt8w12bji68ywof9	eyJ1c2VyIjoxLCJjb21wYW55IjoxfQ:1lJH4G:bx2xljrPnLG9CR7Hbdu2iuXw_vYeH49TIasbSojS1mk	2021-03-22
dlj9xidb2c5c91kmmsw60qu3hk3u9ezt	ZWFlZjZjNDUyMjQ5Y2YyNjc2ZTliOTVhODlhZGIxMGJhOWYyMTlmYTp7Il9hdXRoX3VzZXJfaWQiOiIzIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlNTFkMDViMDc1YThkOWEyMmNhMDk3YzA1MGM5Y2ZlMGU3NDVjMDQ0In0=	2021-03-26
odevuo4b2l5lbn7dckvdquhx9copiptw	NTAxNjQ1MWEyZWUzMWYzZTlhOTc3NmE5M2UxMzU2NTFkMTZkMjViZTp7Il9hdXRoX3VzZXJfaWQiOiI2IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YjkwNjQxOTAxYjM4NGJkOTQ2MjUzYjM5NDQxMGUwZDQxNjAyNjhhIiwidXNlciI6MiwiY29tcGFueSI6NX0=	2021-04-01
9t1rfryzvifyt9lk3nkebbqxw8njvv8x	.eJxVjDkOwyAQAP-ytYXAeDG4TJ83WCwLsXNA5KOIovw9QnLjdmY0X9jXuMDQNhDK6-3zBwZsYPT7No1VjTPDAAZOjHx4xFwF332-FRFK3paZRE3EYVdxLRyfl6M9DSa_TnXbx4TIVnvrSaJRJA1xdLp15DqJyqjOoSVLQUWpLdsUiPsUFOqkWobfH3b1Pk0:1lQsjf:jJYOPiwtPPiRq-O-OLovDlNdiTKK43csb6ZlDDYicEo	2021-04-12
xo2jxxdqakjze2i5szezxff13wo34j6i	.eJxVzDsOwyAQRdG9TG0hMAaDy_RZgzXDQOx8IPKniKLsPUJykbTvPp03jLhv07ivcRlnhgEsNL8bYbjFXANfMV-KCCVvy0yiXsRRV3EuHO-n4_sHTLhOle1jMoadRockjVUkLXH0uvXkO2mUVZ03jhwFFaV27FIg7lNQRifVVrRyMHQNhPJ4Yn7BYD9ftEQ-UA:1lTjQy:nAS05imcYxuaoeX44h1SK-VibusR1mGwshySc5tPsIM	2021-04-20
lzo8jef238ucoet5wqpddux15oedsogo	eyJ1c2VyIjoyLCJjb21wYW55Ijo1fQ:1lUqne:-fPuAVCt-R-7LFPXCBtEKg9FcGGRLQzBNffxDzGNBKU	2021-04-23
nid16w673wfoo95twr39sj52t4z8p4s4	.eJxVjMsOwiAQRf-FdUOgdCi4dO83NDMM2PoA08fCGP9dSbrQ3c09J-clBtzWcdiWOA8Ti4Owovn9CMM15gr4gvlcZCh5nSeSVZE7XeSpcLwdd_cvMOIy1mwfEwA7gw5JgdWkLHH0pvXkOwXa6s6DI0dBR2UcuxSI-xQ0mKTbGq05cYBGhHJ_YH5-9_sDtFA-UA:1lVr01:0iT167eEV4vlfdY_NIE_vDUpGJoxr6bnw9jThkIvbak	2021-04-26
wy6l8vkn6ty9ao9g7mcpplbszn348172	.eJxVjDsOwyAQBe9CHSEwXgwu0-cM1i4LsfOByJ8iinL3iMiNu6c3o_mIbYmz6OEkQnm-ML__e8BtHYeKholFL6w4fIThHnMFfMN8LTKUvM4TyarInS7yUjg-zrt7CIy4jDXbxQTAzqBDUmA1KUscvWk8-VaBtrr14MhR0FEZxy4F4i4FDSbphsX3B3kdPlA:1lWbdt:wnWJ-GYn6nEJb35tBAshDN8Zc8Q3PYLcV4BPIUGHDMo	2021-04-28
kvkz87xakt44qvfoqptbhzudczb5nkv9	.eJxVjEEOwiAQAP_C2RAohYJH730D2WUXqRqalPZk_Lsh6UGvM5N5iwjHXuLReIsLiatw4vLLENKTaxf0gHpfZVrrvi0oeyJP2-S8Er9uZ_s3KNBK306crSVvwAMq6zQqh8TBDAHDqKx2egzWo8ekWRlPPiekKSdtTdYDic8X3Os33A:1lY76N:pvIeIMljNcPnWrTEkcOIQq_aqRnPt-46zIIEp_Q4mQs	2021-05-02
ly0kghv5i7pppqteqaou2ivspw35z59o	eyJ1c2VyIjo1LCJjb21wYW55Ijo1fQ:1lYSvz:3LGSdDx_Vmj-TGsUvylXkDZnxtDH1XF89_uclXQWR8A	2021-05-03
1cuwdit83ms98iogoxdqp9qy44l8rha7	.eJxVjEEOwiAQAP_C2RAohYJH730D2WUXqRqalPZk_Lsh6UGvM5N5iwjHXuLReIsLiatw4vLLENKTaxf0gHpfZVrrvi0oeyJP2-S8Er9uZ_s3KNBK306crSVvwAMq6zQqh8TBDAHDqKx2egzWo8ekWRlPPiekKSdtTdYDic8X3Os33A:1lYlhS:8v9uzjNaLAIF-hyPK9Cxx2l-rlG3EvYcgg0LqsWNnRQ	2021-05-04
8ehd78kgn2nok30tvd912ubpxa8nm3i2	eyJ1c2VyIjo1LCJjb21wYW55Ijo1fQ:1lYm3L:lVn5E92FeAnhFAtdzcPZAxAIV0PYRMUCIOa3x1AKuDs	2021-05-04
\.


--
-- Data for Name: _sqlite_sequence; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._sqlite_sequence (name, seq) FROM stdin;
django_migrations	83
django_admin_log	376
django_content_type	22
auth_permission	92
auth_group	0
auth_user	6
api_role	3
adminpanel_adminuser	12
api_schedule_timelines	50
api_user_friends	2
api_servicecategory	6
api_user	9
api_finishedtrain	36
api_myimage	31
api_company_tags	16
api_company_days	7
api_company_images	5
api_schedule	196
api_timeline	50
api_timer	3
api_company	5
api_traintimer	0
\.


--
-- PostgreSQL database dump complete
--

