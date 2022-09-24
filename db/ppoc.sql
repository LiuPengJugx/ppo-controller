--
-- PostgreSQL database dump
--

-- Dumped from database version 14.1
-- Dumped by pg_dump version 14.1

-- Started on 2022-09-24 19:19:11

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 4 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO postgres;

--
-- TOC entry 3435 (class 0 OID 0)
-- Dependencies: 4
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 221 (class 1259 OID 435147)
-- Name: catalog_sales; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.catalog_sales (
    a0 integer NOT NULL,
    a1 character(4) NOT NULL,
    a2 character(4) NOT NULL,
    a3 character(4) NOT NULL,
    a4 character(4) NOT NULL,
    a5 character(4) NOT NULL,
    a6 character(4) NOT NULL,
    a7 character(4) NOT NULL,
    a8 character(4) NOT NULL,
    a9 character(4) NOT NULL,
    a10 character(4) NOT NULL,
    a11 character(4) NOT NULL,
    a12 character(4) NOT NULL,
    a13 character(4) NOT NULL,
    a14 character(4) NOT NULL,
    a15 character(4) NOT NULL,
    a16 character(4) NOT NULL,
    a17 character(8) NOT NULL,
    a18 character(4) NOT NULL,
    a19 character(7) NOT NULL,
    a20 character(7) NOT NULL,
    a21 character(7) NOT NULL,
    a22 character(7) NOT NULL,
    a23 character(7) NOT NULL,
    a24 character(7) NOT NULL,
    a25 character(7) NOT NULL,
    a26 character(7) NOT NULL,
    a27 character(7) NOT NULL,
    a28 character(7) NOT NULL,
    a29 character(7) NOT NULL,
    a30 character(7) NOT NULL,
    a31 character(7) NOT NULL,
    a32 character(7) NOT NULL,
    a33 character(7) NOT NULL
);


ALTER TABLE public.catalog_sales OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 435146)
-- Name: catalog_sales_a0_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.catalog_sales_a0_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.catalog_sales_a0_seq OWNER TO postgres;

--
-- TOC entry 3436 (class 0 OID 0)
-- Dependencies: 220
-- Name: catalog_sales_a0_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.catalog_sales_a0_seq OWNED BY public.catalog_sales.a0;


--
-- TOC entry 215 (class 1259 OID 435126)
-- Name: lineitem; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.lineitem (
    a0 integer NOT NULL,
    a1 character(8) NOT NULL,
    a2 character(8) NOT NULL,
    a3 character(4) NOT NULL,
    a4 character(15) NOT NULL,
    a5 character(15) NOT NULL,
    a6 character(15) NOT NULL,
    a7 character(15) NOT NULL,
    a8 character(1) NOT NULL,
    a9 character(1) NOT NULL,
    a10 character(10) NOT NULL,
    a11 character(10) NOT NULL,
    a12 character(10) NOT NULL,
    a13 character(25) NOT NULL,
    a14 character(10) NOT NULL,
    a15 character(44) NOT NULL
);


ALTER TABLE public.lineitem OWNER TO postgres;

--
-- TOC entry 214 (class 1259 OID 435125)
-- Name: lineitem_a0_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.lineitem_a0_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.lineitem_a0_seq OWNER TO postgres;

--
-- TOC entry 3437 (class 0 OID 0)
-- Dependencies: 214
-- Name: lineitem_a0_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.lineitem_a0_seq OWNED BY public.lineitem.a0;


--
-- TOC entry 217 (class 1259 OID 435133)
-- Name: orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders (
    a0 integer NOT NULL,
    a1 character(4) NOT NULL,
    a2 character(1) NOT NULL,
    a3 character(4) NOT NULL,
    a4 character(10) NOT NULL,
    a5 character(15) NOT NULL,
    a6 character(15) NOT NULL,
    a7 character(4) NOT NULL,
    a8 character(79) NOT NULL
);


ALTER TABLE public.orders OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 435132)
-- Name: orders_a0_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.orders_a0_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.orders_a0_seq OWNER TO postgres;

--
-- TOC entry 3438 (class 0 OID 0)
-- Dependencies: 216
-- Name: orders_a0_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.orders_a0_seq OWNED BY public.orders.a0;



--
-- TOC entry 223 (class 1259 OID 435155)
-- Name: store_sales; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.store_sales (
    a0 integer NOT NULL,
    a1 character(4) NOT NULL,
    a2 character(4) NOT NULL,
    a3 character(4) NOT NULL,
    a4 character(4) NOT NULL,
    a5 character(4) NOT NULL,
    a6 character(4) NOT NULL,
    a7 character(4) NOT NULL,
    a8 character(4) NOT NULL,
    a9 character(8) NOT NULL,
    a10 character(4) NOT NULL,
    a11 character(7) NOT NULL,
    a12 character(7) NOT NULL,
    a13 character(7) NOT NULL,
    a14 character(7) NOT NULL,
    a15 character(7) NOT NULL,
    a16 character(7) NOT NULL,
    a17 character(7) NOT NULL,
    a18 character(7) NOT NULL,
    a19 character(7) NOT NULL,
    a20 character(7) NOT NULL,
    a21 character(7) NOT NULL,
    a22 character(7) NOT NULL
);


ALTER TABLE public.store_sales OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 622432)
-- Name: store_sales0; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.store_sales0 (
    a0 integer NOT NULL,
    a1 character(4) NOT NULL,
    a2 character(4) NOT NULL,
    a3 character(4) NOT NULL,
    a4 character(4) NOT NULL,
    a5 character(4) NOT NULL,
    a6 character(4) NOT NULL,
    a7 character(4) NOT NULL,
    a8 character(4) NOT NULL,
    a9 character(8) NOT NULL,
    a10 character(4) NOT NULL,
    a11 character(7) NOT NULL,
    a12 character(7) NOT NULL,
    a13 character(7) NOT NULL,
    a14 character(7) NOT NULL,
    a15 character(7) NOT NULL,
    a16 character(7) NOT NULL,
    a17 character(7) NOT NULL,
    a18 character(7) NOT NULL,
    a19 character(7) NOT NULL,
    a20 character(7) NOT NULL,
    a21 character(7) NOT NULL,
    a22 character(7) NOT NULL
);


ALTER TABLE public.store_sales0 OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 622431)
-- Name: store_sales0_a0_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.store_sales0_a0_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.store_sales0_a0_seq OWNER TO postgres;

--
-- TOC entry 3439 (class 0 OID 0)
-- Dependencies: 226
-- Name: store_sales0_a0_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.store_sales0_a0_seq OWNED BY public.store_sales0.a0;


--
-- TOC entry 229 (class 1259 OID 622439)
-- Name: store_sales1; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.store_sales1 (
    a0 integer NOT NULL,
    a1 character(4) NOT NULL,
    a2 character(4) NOT NULL,
    a3 character(4) NOT NULL,
    a4 character(4) NOT NULL,
    a5 character(4) NOT NULL,
    a6 character(4) NOT NULL,
    a7 character(4) NOT NULL,
    a8 character(4) NOT NULL,
    a9 character(8) NOT NULL,
    a10 character(4) NOT NULL,
    a11 character(7) NOT NULL,
    a12 character(7) NOT NULL,
    a13 character(7) NOT NULL,
    a14 character(7) NOT NULL,
    a15 character(7) NOT NULL,
    a16 character(7) NOT NULL,
    a17 character(7) NOT NULL,
    a18 character(7) NOT NULL,
    a19 character(7) NOT NULL,
    a20 character(7) NOT NULL,
    a21 character(7) NOT NULL,
    a22 character(7) NOT NULL
);


ALTER TABLE public.store_sales1 OWNER TO postgres;

--
-- TOC entry 228 (class 1259 OID 622438)
-- Name: store_sales1_a0_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.store_sales1_a0_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.store_sales1_a0_seq OWNER TO postgres;

--
-- TOC entry 3440 (class 0 OID 0)
-- Dependencies: 228
-- Name: store_sales1_a0_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.store_sales1_a0_seq OWNED BY public.store_sales1.a0;


--
-- TOC entry 231 (class 1259 OID 622446)
-- Name: store_sales2; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.store_sales2 (
    a0 integer NOT NULL,
    a1 character(4) NOT NULL,
    a2 character(4) NOT NULL,
    a3 character(4) NOT NULL,
    a4 character(4) NOT NULL,
    a5 character(4) NOT NULL,
    a6 character(4) NOT NULL,
    a7 character(4) NOT NULL,
    a8 character(4) NOT NULL,
    a9 character(8) NOT NULL,
    a10 character(4) NOT NULL,
    a11 character(7) NOT NULL,
    a12 character(7) NOT NULL,
    a13 character(7) NOT NULL,
    a14 character(7) NOT NULL,
    a15 character(7) NOT NULL,
    a16 character(7) NOT NULL,
    a17 character(7) NOT NULL,
    a18 character(7) NOT NULL,
    a19 character(7) NOT NULL,
    a20 character(7) NOT NULL,
    a21 character(7) NOT NULL,
    a22 character(7) NOT NULL
);


ALTER TABLE public.store_sales2 OWNER TO postgres;

--
-- TOC entry 230 (class 1259 OID 622445)
-- Name: store_sales2_a0_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.store_sales2_a0_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.store_sales2_a0_seq OWNER TO postgres;

--
-- TOC entry 3441 (class 0 OID 0)
-- Dependencies: 230
-- Name: store_sales2_a0_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.store_sales2_a0_seq OWNED BY public.store_sales2.a0;


--
-- TOC entry 233 (class 1259 OID 622453)
-- Name: store_sales3; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.store_sales3 (
    a0 integer NOT NULL,
    a1 character(4) NOT NULL,
    a2 character(4) NOT NULL,
    a3 character(4) NOT NULL,
    a4 character(4) NOT NULL,
    a5 character(4) NOT NULL,
    a6 character(4) NOT NULL,
    a7 character(4) NOT NULL,
    a8 character(4) NOT NULL,
    a9 character(8) NOT NULL,
    a10 character(4) NOT NULL,
    a11 character(7) NOT NULL,
    a12 character(7) NOT NULL,
    a13 character(7) NOT NULL,
    a14 character(7) NOT NULL,
    a15 character(7) NOT NULL,
    a16 character(7) NOT NULL,
    a17 character(7) NOT NULL,
    a18 character(7) NOT NULL,
    a19 character(7) NOT NULL,
    a20 character(7) NOT NULL,
    a21 character(7) NOT NULL,
    a22 character(7) NOT NULL
);


ALTER TABLE public.store_sales3 OWNER TO postgres;

--
-- TOC entry 232 (class 1259 OID 622452)
-- Name: store_sales3_a0_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.store_sales3_a0_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.store_sales3_a0_seq OWNER TO postgres;

--
-- TOC entry 3442 (class 0 OID 0)
-- Dependencies: 232
-- Name: store_sales3_a0_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.store_sales3_a0_seq OWNED BY public.store_sales3.a0;


--
-- TOC entry 235 (class 1259 OID 622460)
-- Name: store_sales4; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.store_sales4 (
    a0 integer NOT NULL,
    a1 character(4) NOT NULL,
    a2 character(4) NOT NULL,
    a3 character(4) NOT NULL,
    a4 character(4) NOT NULL,
    a5 character(4) NOT NULL,
    a6 character(4) NOT NULL,
    a7 character(4) NOT NULL,
    a8 character(4) NOT NULL,
    a9 character(8) NOT NULL,
    a10 character(4) NOT NULL,
    a11 character(7) NOT NULL,
    a12 character(7) NOT NULL,
    a13 character(7) NOT NULL,
    a14 character(7) NOT NULL,
    a15 character(7) NOT NULL,
    a16 character(7) NOT NULL,
    a17 character(7) NOT NULL,
    a18 character(7) NOT NULL,
    a19 character(7) NOT NULL,
    a20 character(7) NOT NULL,
    a21 character(7) NOT NULL,
    a22 character(7) NOT NULL
);


ALTER TABLE public.store_sales4 OWNER TO postgres;

--
-- TOC entry 234 (class 1259 OID 622459)
-- Name: store_sales4_a0_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.store_sales4_a0_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.store_sales4_a0_seq OWNER TO postgres;

--
-- TOC entry 3443 (class 0 OID 0)
-- Dependencies: 234
-- Name: store_sales4_a0_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.store_sales4_a0_seq OWNED BY public.store_sales4.a0;


--
-- TOC entry 222 (class 1259 OID 435154)
-- Name: store_sales_a0_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.store_sales_a0_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.store_sales_a0_seq OWNER TO postgres;

--
-- TOC entry 3444 (class 0 OID 0)
-- Dependencies: 222
-- Name: store_sales_a0_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.store_sales_a0_seq OWNED BY public.store_sales.a0;


--
-- TOC entry 236 (class 1259 OID 662116)
-- Name: student; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.student (
    sno character(9) NOT NULL,
    sname character(10) NOT NULL,
    ssex character(2),
    sage numeric(2,0),
    sdept character(2)
);


ALTER TABLE public.student OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 435140)
-- Name: supplier; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.supplier (
    a0 integer NOT NULL,
    a1 character(25) NOT NULL,
    a2 character(40) NOT NULL,
    a3 character(4) NOT NULL,
    a4 character(15) NOT NULL,
    a5 character(4) NOT NULL,
    a6 character(101) NOT NULL
);


ALTER TABLE public.supplier OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 435139)
-- Name: supplier_a0_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.supplier_a0_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.supplier_a0_seq OWNER TO postgres;

--
-- TOC entry 3445 (class 0 OID 0)
-- Dependencies: 218
-- Name: supplier_a0_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.supplier_a0_seq OWNED BY public.supplier.a0;


--
-- TOC entry 212 (class 1259 OID 16395)
-- Name: tt_tab; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tt_tab (
    a0 integer NOT NULL,
    a1 character(4) NOT NULL,
    a2 character(4) NOT NULL,
    a3 character(4) NOT NULL,
    a4 character(4) NOT NULL,
    a5 character(4) NOT NULL,
    a6 character(4) NOT NULL,
    a7 character(4) NOT NULL,
    a8 character(4) NOT NULL,
    a9 character(4) NOT NULL,
    a10 character(4) NOT NULL,
    a11 character(4) NOT NULL,
    a12 character(4) NOT NULL,
    a13 character(4) NOT NULL,
    a14 character(4) NOT NULL,
    a15 character(4) NOT NULL,
    a16 character(4) NOT NULL,
    a17 character(4) NOT NULL,
    a18 character(4) NOT NULL,
    a19 character(4) NOT NULL,
    a20 character(4) NOT NULL,
    a21 character(4) NOT NULL,
    a22 character(4) NOT NULL,
    a23 character(4) NOT NULL,
    a24 character(4) NOT NULL,
    a25 character(4) NOT NULL,
    a26 character(4) NOT NULL,
    a27 character(4) NOT NULL,
    a28 character(4) NOT NULL,
    a29 character(4) NOT NULL,
    a30 character(4) NOT NULL,
    a31 character(4) NOT NULL,
    a32 character(4) NOT NULL,
    a33 character(4) NOT NULL,
    a34 character(4) NOT NULL,
    a35 character(4) NOT NULL,
    a36 character(4) NOT NULL,
    a37 character(4) NOT NULL,
    a38 character(4) NOT NULL,
    a39 character(4) NOT NULL,
    a40 character(4) NOT NULL,
    a41 character(4) NOT NULL,
    a42 character(4) NOT NULL,
    a43 character(4) NOT NULL,
    a44 character(4) NOT NULL,
    a45 character(4) NOT NULL,
    a46 character(4) NOT NULL,
    a47 character(4) NOT NULL,
    a48 character(4) NOT NULL,
    a49 character(4) NOT NULL
);


ALTER TABLE public.tt_tab OWNER TO postgres;

--
-- TOC entry 211 (class 1259 OID 16394)
-- Name: tt_tab_a0_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tt_tab_a0_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tt_tab_a0_seq OWNER TO postgres;

--
-- TOC entry 3446 (class 0 OID 0)
-- Dependencies: 211
-- Name: tt_tab_a0_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tt_tab_a0_seq OWNED BY public.tt_tab.a0;


--
-- TOC entry 225 (class 1259 OID 435162)
-- Name: web_sales; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.web_sales (
    a0 integer NOT NULL,
    a1 character(4) NOT NULL,
    a2 character(4) NOT NULL,
    a3 character(4) NOT NULL,
    a4 character(4) NOT NULL,
    a5 character(4) NOT NULL,
    a6 character(4) NOT NULL,
    a7 character(4) NOT NULL,
    a8 character(4) NOT NULL,
    a9 character(4) NOT NULL,
    a10 character(4) NOT NULL,
    a11 character(4) NOT NULL,
    a12 character(4) NOT NULL,
    a13 character(4) NOT NULL,
    a14 character(4) NOT NULL,
    a15 character(4) NOT NULL,
    a16 character(4) NOT NULL,
    a17 character(8) NOT NULL,
    a18 character(4) NOT NULL,
    a19 character(7) NOT NULL,
    a20 character(7) NOT NULL,
    a21 character(7) NOT NULL,
    a22 character(7) NOT NULL,
    a23 character(7) NOT NULL,
    a24 character(7) NOT NULL,
    a25 character(7) NOT NULL,
    a26 character(7) NOT NULL,
    a27 character(7) NOT NULL,
    a28 character(7) NOT NULL,
    a29 character(7) NOT NULL,
    a30 character(7) NOT NULL,
    a31 character(7) NOT NULL,
    a32 character(7) NOT NULL,
    a33 character(7) NOT NULL
);


ALTER TABLE public.web_sales OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 435161)
-- Name: web_sales_a0_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.web_sales_a0_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.web_sales_a0_seq OWNER TO postgres;

--
-- TOC entry 3447 (class 0 OID 0)
-- Dependencies: 224
-- Name: web_sales_a0_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.web_sales_a0_seq OWNED BY public.web_sales.a0;


--
-- TOC entry 3257 (class 2604 OID 435150)
-- Name: catalog_sales a0; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.catalog_sales ALTER COLUMN a0 SET DEFAULT nextval('public.catalog_sales_a0_seq'::regclass);


--
-- TOC entry 3254 (class 2604 OID 435129)
-- Name: lineitem a0; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lineitem ALTER COLUMN a0 SET DEFAULT nextval('public.lineitem_a0_seq'::regclass);


--
-- TOC entry 3255 (class 2604 OID 435136)
-- Name: orders a0; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders ALTER COLUMN a0 SET DEFAULT nextval('public.orders_a0_seq'::regclass);


--
-- TOC entry 3258 (class 2604 OID 435158)
-- Name: store_sales a0; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.store_sales ALTER COLUMN a0 SET DEFAULT nextval('public.store_sales_a0_seq'::regclass);


--
-- TOC entry 3260 (class 2604 OID 622435)
-- Name: store_sales0 a0; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.store_sales0 ALTER COLUMN a0 SET DEFAULT nextval('public.store_sales0_a0_seq'::regclass);


--
-- TOC entry 3261 (class 2604 OID 622442)
-- Name: store_sales1 a0; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.store_sales1 ALTER COLUMN a0 SET DEFAULT nextval('public.store_sales1_a0_seq'::regclass);


--
-- TOC entry 3262 (class 2604 OID 622449)
-- Name: store_sales2 a0; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.store_sales2 ALTER COLUMN a0 SET DEFAULT nextval('public.store_sales2_a0_seq'::regclass);


--
-- TOC entry 3263 (class 2604 OID 622456)
-- Name: store_sales3 a0; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.store_sales3 ALTER COLUMN a0 SET DEFAULT nextval('public.store_sales3_a0_seq'::regclass);


--
-- TOC entry 3264 (class 2604 OID 622463)
-- Name: store_sales4 a0; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.store_sales4 ALTER COLUMN a0 SET DEFAULT nextval('public.store_sales4_a0_seq'::regclass);


--
-- TOC entry 3256 (class 2604 OID 435143)
-- Name: supplier a0; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.supplier ALTER COLUMN a0 SET DEFAULT nextval('public.supplier_a0_seq'::regclass);


--
-- TOC entry 3253 (class 2604 OID 16398)
-- Name: tt_tab a0; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tt_tab ALTER COLUMN a0 SET DEFAULT nextval('public.tt_tab_a0_seq'::regclass);


--
-- TOC entry 3259 (class 2604 OID 435165)
-- Name: web_sales a0; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.web_sales ALTER COLUMN a0 SET DEFAULT nextval('public.web_sales_a0_seq'::regclass);


--
-- TOC entry 3274 (class 2606 OID 435152)
-- Name: catalog_sales catalog_sales_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.catalog_sales
    ADD CONSTRAINT catalog_sales_pkey PRIMARY KEY (a0);


--
-- TOC entry 3268 (class 2606 OID 435131)
-- Name: lineitem lineitem_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lineitem
    ADD CONSTRAINT lineitem_pkey PRIMARY KEY (a0);


--
-- TOC entry 3270 (class 2606 OID 435138)
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (a0);


--
-- TOC entry 3280 (class 2606 OID 622437)
-- Name: store_sales0 store_sales0_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.store_sales0
    ADD CONSTRAINT store_sales0_pkey PRIMARY KEY (a0);


--
-- TOC entry 3282 (class 2606 OID 622444)
-- Name: store_sales1 store_sales1_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.store_sales1
    ADD CONSTRAINT store_sales1_pkey PRIMARY KEY (a0);


--
-- TOC entry 3284 (class 2606 OID 622451)
-- Name: store_sales2 store_sales2_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.store_sales2
    ADD CONSTRAINT store_sales2_pkey PRIMARY KEY (a0);


--
-- TOC entry 3286 (class 2606 OID 622458)
-- Name: store_sales3 store_sales3_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.store_sales3
    ADD CONSTRAINT store_sales3_pkey PRIMARY KEY (a0);


--
-- TOC entry 3288 (class 2606 OID 622465)
-- Name: store_sales4 store_sales4_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.store_sales4
    ADD CONSTRAINT store_sales4_pkey PRIMARY KEY (a0);


--
-- TOC entry 3276 (class 2606 OID 435160)
-- Name: store_sales store_sales_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.store_sales
    ADD CONSTRAINT store_sales_pkey PRIMARY KEY (a0);


--
-- TOC entry 3290 (class 2606 OID 662120)
-- Name: student studentkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student
    ADD CONSTRAINT studentkey PRIMARY KEY (sno);


--
-- TOC entry 3272 (class 2606 OID 435145)
-- Name: supplier supplier_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.supplier
    ADD CONSTRAINT supplier_pkey PRIMARY KEY (a0);


--
-- TOC entry 3266 (class 2606 OID 16400)
-- Name: tt_tab tt_tab_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tt_tab
    ADD CONSTRAINT tt_tab_pkey PRIMARY KEY (a0);


--
-- TOC entry 3278 (class 2606 OID 435167)
-- Name: web_sales web_sales_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.web_sales
    ADD CONSTRAINT web_sales_pkey PRIMARY KEY (a0);


-- Completed on 2022-09-24 19:19:11

--
-- PostgreSQL database dump complete
--

