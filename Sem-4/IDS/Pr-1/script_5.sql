-------------------------------------------------------------------------------------------------------------
-- procedure drops a table only if it exists
CREATE OR REPLACE PROCEDURE DROP_IF_EXISTS(tableName VARCHAR2)
IS
    counter number := 0;
begin
    select count(*) into counter from user_tables where table_name = upper(tableName);
    if counter > 0 then
        EXECUTE IMMEDIATE 'DROP TABLE ' || tableName || ' CASCADE CONSTRAINTS';
    end if;
end;
/

-------------------------------------------------------------------------------------------------------------
-- TABLES

-- ZAMESTNANEC
-- id, meno, priezvisko, pozicia, datum narodenia, telefon, cislo uctu
BEGIN DROP_IF_EXISTS('zamestnanec'); END;
CREATE TABLE zamestnanec (
    id INT DEFAULT NULL,
    meno VARCHAR2(50) NOT NULL,
    priezvisko VARCHAR2(50) NOT NULL,
    pozicia VARCHAR2(10) NOT NULL,
    datum_narodenia DATE NOT NULL,
    telefon VARCHAR2(13) NOT NULL,
    cislo_uctu VARCHAR2(24) NOT NULL,
    CONSTRAINT zamestnanec_pk PRIMARY KEY (id),
    CONSTRAINT pozicia_chk CHECK (pozicia IN ('manazer', 'skladnik')),
    CONSTRAINT zamestnanec_telefon_chk CHECK (REGEXP_LIKE(telefon, '^\+420\d{9}$')),
    CONSTRAINT cislo_uctu_chk CHECK (REGEXP_LIKE(cislo_uctu, '^CZ\d{22}$'))
);
/

-- DODAVATEL
-- id, nazov, adresa, telefon
BEGIN DROP_IF_EXISTS('dodavatel'); END;
CREATE TABLE dodavatel (
    id NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) NOT NULL,
    nazov VARCHAR2(50) NOT NULL,
    ulica VARCHAR2(50) DEFAULT NULL,
    cislo_ulice NUMBER NOT NULL,
    mesto VARCHAR2(50) NOT NULL,
    psc NUMBER(5) NOT NULL,
    telefon VARCHAR2(13) NOT NULL,
    CONSTRAINT dodavatel_pk PRIMARY KEY (id),
    CONSTRAINT dodavatel_telefon_chk CHECK (REGEXP_LIKE(telefon, '^\+420\d{9}$')),
    CONSTRAINT dodavatel_psc_chk CHECK (REGEXP_LIKE(psc, '^\d{5}$'))
);
/

-- OBJEDNAVKA
-- ic, datum vytvorenia, suma, stav
BEGIN DROP_IF_EXISTS('objednavka'); END;
CREATE TABLE objednavka (
    ic NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) NOT NULL,
    stav VARCHAR2(10) NOT NULL,
    datum_vytvorenia DATE NOT NULL,
    suma NUMBER(10,2) NOT NULL,
    zamestnanec_fk NUMBER NOT NULL,
    dodavatel_fk NUMBER DEFAULT NULL,
    CONSTRAINT objednavka_pk PRIMARY KEY (ic),
    CONSTRAINT zamestnanec_fk FOREIGN KEY(zamestnanec_fk) REFERENCES zamestnanec(id),
    CONSTRAINT dodavatel_prijal_fk FOREIGN KEY(dodavatel_fk) REFERENCES dodavatel(id),
    CONSTRAINT objednavka_stav_chk CHECK (stav IN ('vytvorena', 'odoslana', 'spracovana', 'dorucena'))
);
/

-- BUDOVA
-- ic, nazov, adresa, kapacita
BEGIN DROP_IF_EXISTS('budova'); END;
CREATE TABLE budova (
    ic NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) NOT NULL,
    meno VARCHAR2(20) NOT NULL,
    ulica VARCHAR2(50) DEFAULT NULL,
    cislo_ulice NUMBER NOT NULL,
    mesto VARCHAR2(50) NOT NULL,
    psc NUMBER(5) NOT NULL,
    kapacita NUMBER NOT NULL,
    CONSTRAINT budova_pk PRIMARY KEY (ic),
    CONSTRAINT budova_psc_chk CHECK (REGEXP_LIKE(psc, '^\d{5}$')),
    CONSTRAINT kapacita_chk CHECK (kapacita > 0)
);
/

-- ZIADOST O PRESUN TOVARU
-- ic, stav, datum vytvorenia, pocet bochnikov
BEGIN DROP_IF_EXISTS('presun_tovaru'); END;
CREATE TABLE presun_tovaru (
    ic NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) NOT NULL,
    stav VARCHAR2(10) NOT NULL,
    datum_vytvorenia DATE NOT NULL,
    pocet_bochnikov NUMBER NOT NULL,
    zamestnanec_poziadal_fk NUMBER NOT NULL,
    zamestnanec_vykonal_fk NUMBER DEFAULT NULL,
    presun_z_fk NUMBER NOT NULL,
    presun_do_fk NUMBER NOT NULL,
    CONSTRAINT presun_tovaru_pk PRIMARY KEY (ic),
    CONSTRAINT zamestnanec_poziadal_fk FOREIGN KEY(zamestnanec_poziadal_fk) REFERENCES zamestnanec(id),
    CONSTRAINT zamestnanec_vykonal_fk FOREIGN KEY(zamestnanec_vykonal_fk) REFERENCES zamestnanec(id),
    CONSTRAINT presun_z_fk FOREIGN KEY(presun_z_fk) REFERENCES budova(ic),
    CONSTRAINT presun_do_fk FOREIGN KEY(presun_do_fk) REFERENCES budova(ic),
    CONSTRAINT presun_stav_chk CHECK (stav IN ('vytvorena', 'potvrdena', 'vykonana')),
    CONSTRAINT pocet_bochnikov_chk CHECK (pocet_bochnikov > 0)
);
/

-- KRAJINA POVODU
-- ic, nazov, kontinent, podnebie
BEGIN DROP_IF_EXISTS('krajina_povodu'); END;
CREATE TABLE krajina_povodu (
    ic NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) NOT NULL,
    nazov VARCHAR2(30) NOT NULL,
    kontinent VARCHAR2(20) NOT NULL,
    podnebie VARCHAR2(30) NOT NULL,
    CONSTRAINT krajina_povodu_pk PRIMARY KEY (ic)
);
/

-- DRUH SYRA
-- ic, nazov, zivocich, percento tuku, doba udenia
BEGIN DROP_IF_EXISTS('druh_syra'); END;
CREATE TABLE druh_syra (
    ic NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) NOT NULL,
    meno VARCHAR2(30) NOT NULL,
    zivocich VARCHAR2(30) NOT NULL,
    percento_tuku NUMBER NOT NULL,
    doba_udenia NUMBER DEFAULT 0,
    krajina_povodu_fk NUMBER NOT NULL,
    CONSTRAINT druh_syra_pk PRIMARY KEY (ic),
    CONSTRAINT krajina_povodu_fk FOREIGN KEY(krajina_povodu_fk) REFERENCES krajina_povodu(ic),
    CONSTRAINT percento_tuku_chk CHECK (0 <= percento_tuku AND percento_tuku <= 100),
    CONSTRAINT doba_udenia_chk CHECK (0 <= doba_udenia)
);
/

-- BOCHNIK
-- ic, pociatocna hmotnost, aktualna hmotnost, datum dodania, datum spotreby
BEGIN DROP_IF_EXISTS('bochnik'); END;
CREATE TABLE bochnik (
    ic NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) NOT NULL,
    pociatocna_hmotnost NUMBER(5, 2) NOT NULL,
    aktualna_hmotnost NUMBER(5, 2) NOT NULL,
    datum_dodania DATE NOT NULL,
    datum_spotreby DATE NOT NULL,
    druh_syra_fk NUMBER NOT NULL,
    budova_fk NUMBER NOT NULL,
    dodavatel_fk NUMBER NOT NULL,
    CONSTRAINT bochnik_pk PRIMARY KEY (ic),
    CONSTRAINT druh_syra_fk FOREIGN KEY(druh_syra_fk) REFERENCES druh_syra(ic),
    CONSTRAINT budova_fk FOREIGN KEY(budova_fk) REFERENCES budova(ic),
    CONSTRAINT dodavatel_fk FOREIGN KEY(dodavatel_fk) REFERENCES dodavatel(id)
);
/

-- DRUH SYRA V OBJEDNAVKA
-- hmotnost
BEGIN DROP_IF_EXISTS('druh_syra_v_objednavke'); END;
CREATE TABLE druh_syra_v_objednavke (
    objednavka_fk NUMBER NOT NULL,
    druh_syra_fk NUMBER NOT NULL,
    hmotnost NUMBER NOT NULL,
    CONSTRAINT druh_syra_v_objednavke_pk PRIMARY KEY (objednavka_fk, druh_syra_fk),
    CONSTRAINT objednavka_fk FOREIGN KEY(objednavka_fk) REFERENCES objednavka(ic),
    CONSTRAINT druh_syra_v_objednavke_fk FOREIGN KEY(druh_syra_fk) REFERENCES druh_syra(ic)
);
/

-- NADRADENY ZAMESTNANEC
-- -
BEGIN DROP_IF_EXISTS('nadradeny_zamestnanec'); END;
CREATE TABLE nadradeny_zamestnanec (
    nadradeny_zamestnanec_fk NUMBER NOT NULL,
    podradeny_zamestnanec_fk NUMBER NOT NULL,
    CONSTRAINT nadradeny_zamestnanec_pk PRIMARY KEY (podradeny_zamestnanec_fk, nadradeny_zamestnanec_fk),
    CONSTRAINT nadradeny_zamestnanec_fk FOREIGN KEY(nadradeny_zamestnanec_fk) REFERENCES zamestnanec(id),
    CONSTRAINT podradeny_zamestnanec_fk FOREIGN KEY(podradeny_zamestnanec_fk) REFERENCES zamestnanec(id)
);
/

-- PRESUN BOCHNIKA
-- -
BEGIN DROP_IF_EXISTS('presun_bochnika'); END;
CREATE TABLE presun_bochnika (
    presun_fk NUMBER NOT NULL,
    bochnik_fk NUMBER NOT NULL,
    CONSTRAINT presun_bochnika_pk PRIMARY KEY (presun_fk, bochnik_fk),
    CONSTRAINT presun_fk FOREIGN KEY(presun_fk) REFERENCES presun_tovaru(ic),
    CONSTRAINT bochnik_fk FOREIGN KEY(bochnik_fk) REFERENCES bochnik(ic)
);
/


-------------------------------------------------------------------------------------------------------------
-- TRIGGERS

-- trigger 1
-- checks IBAN according to: 'https://www.kutac.cz/pocitace-a-internety/generovani-a-kontrola-ibanu-pro-cz-i-sk-ucty'
CREATE OR REPLACE TRIGGER Check_cislo_uctu
    BEFORE INSERT OR UPDATE OF cislo_uctu ON zamestnanec
    FOR EACH ROW
    DECLARE
        string VARCHAR2(26);
        num NUMBER;
        nespravne_cislo Exception;
    BEGIN
        string := substr(:NEW.cislo_uctu, 5) || '12' || '35' || substr(:NEW.cislo_uctu, 3, 2);
        num := TO_NUMBER(string);
        IF ((num mod 97) != 1) THEN
            RAISE nespravne_cislo;
        END IF;
    EXCEPTION
        WHEN nespravne_cislo THEN
            RAISE_APPLICATION_ERROR(-20000, 'Nesprávne číslo účtu: ' || :NEW.cislo_uctu);
    END;
/


-- trigger 2
-- creating (+ drop if exists) sequence used in trigger 2
DECLARE
    counter NUMBER := 0;
BEGIN
    SELECT COUNT(*) INTO counter FROM USER_SEQUENCES WHERE SEQUENCE_NAME = 'ID_SEKVENCIA';
    IF counter > 0 then
        EXECUTE IMMEDIATE 'DROP SEQUENCE ID_SEKVENCIA';
    END IF;
END;
CREATE SEQUENCE id_sekvencia;

-- trigger for automatic generation of primary key values in table zamestnanec
CREATE OR REPLACE TRIGGER Generate_zamestnanec_id
    BEFORE INSERT ON zamestnanec
    FOR EACH ROW
BEGIN
	IF :NEW.id IS NULL THEN
        :NEW.id := id_sekvencia.nextval;
	END IF;
END;
/


-------------------------------------------------------------------------------------------------------------
-- PROCEDURES

-- procedure prints number of orders containing the chosen cheese type
CREATE OR REPLACE PROCEDURE CHEESE_TYPE_IN_ORDERS(cheese_type_input VARCHAR)
AS
    order_count NUMBER := 0;
    all_orders NUMBER;
	cheese_type druh_syra.ic%TYPE;
    chosen_cheese_type druh_syra.ic%TYPE;
    CURSOR cheese_type_cursor IS SELECT druh_syra_fk FROM druh_syra_v_objednavke;
BEGIN
	SELECT ic INTO chosen_cheese_type FROM druh_syra WHERE meno = cheese_type_input;

	SELECT COUNT(*) INTO all_orders FROM objednavka;

    OPEN cheese_type_cursor;
    LOOP
        FETCH cheese_type_cursor INTO cheese_type;

        IF cheese_type_cursor%NOTFOUND THEN
            EXIT;
        END IF;

        IF cheese_type = chosen_cheese_type THEN
            order_count := order_count + 1;
        END IF;
    END LOOP;
    CLOSE cheese_type_cursor;

    dbms_output.put_line('Druh syra ' || cheese_type_input || ' sa vyskytuje v ' || order_count || ' objednavkach.');

    EXCEPTION
	-- invalid cheese type
	WHEN NO_DATA_FOUND THEN
        dbms_output.put_line('Druh syra ' || cheese_type_input || ' nepredavame.');
END;
/


-- procedure prints percentage of cheese wheels of chosen cheese type in all warehouses
CREATE OR REPLACE PROCEDURE PERCENTAGE_OF_CHEESE_TYPE(cheese_type_input VARCHAR)
AS
    chosen_cheeses NUMBER;
    all_cheeses NUMBER;
    percentage DECIMAL;
    chosen_cheese_type druh_syra.ic%TYPE;
BEGIN
	SELECT ic INTO chosen_cheese_type FROM druh_syra WHERE meno = cheese_type_input;

    SELECT COUNT(*) INTO all_cheeses FROM bochnik;
    SELECT COUNT(*) INTO chosen_cheeses FROM bochnik WHERE druh_syra_fk = chosen_cheese_type;

	percentage := chosen_cheeses / all_cheeses * 100;

    dbms_output.put_line('Druh syra ' || cheese_type_input || ' tvori ' || percentage || '% vsetkych bochnikov na sklade.');

	EXCEPTION
    -- no cheese wheels in stock
    WHEN ZERO_DIVIDE THEN
        dbms_output.put_line('Na sklade momentalne nie su ziadne bochniky.');
	-- invalid cheese type
	WHEN NO_DATA_FOUND THEN
        dbms_output.put_line('Druh syra ' || cheese_type_input || ' nepredavame.');
END;
/


-------------------------------------------------------------------------------------------------------------
-- EXEMPLARY DATA INSERTION

DECLARE
    jessie_id NUMBER;
    pete_id NUMBER;
    gus_id NUMBER;
    madrigal_id NUMBER;
    sklad_a_ic NUMBER;
    sklad_b_ic NUMBER;
    rakusko_ic NUMBER;
    svajciarsko_ic NUMBER;
    gouda_ic NUMBER;
    ostiepok_ic NUMBER;
    gouda2_ic NUMBER;
    ostiepok2_ic NUMBER;
    objednavka_1_ic NUMBER;
    objednavka_2_ic NUMBER;
    bochnik_1_ic NUMBER;
    presun_1_ic NUMBER;

BEGIN
    INSERT INTO zamestnanec VALUES (DEFAULT ,'Jesse', 'Pinkman', 'skladnik', TO_DATE('24.09.1984','DD.MM.YYYY'), '+420012345678', 'CZ0850517625838814166353')
    RETURNING id INTO jessie_id;
    INSERT INTO zamestnanec VALUES (DEFAULT, 'Pete', 'Skinny', 'skladnik', TO_DATE('30.12.1983','DD.MM.YYYY'), '+420012345689', 'CZ7950512266969511936981')
    RETURNING id INTO pete_id;
    INSERT INTO zamestnanec VALUES (DEFAULT, 'Gus', 'Fring', 'manazer', TO_DATE('01.04.1970','DD.MM.YYYY'), '+420445678901', 'CZ0650515784213998216812')
    RETURNING id INTO gus_id;

    INSERT INTO nadradeny_zamestnanec VALUES (gus_id, jessie_id);
    INSERT INTO nadradeny_zamestnanec VALUES (gus_id, pete_id);

    INSERT INTO budova VALUES (DEFAULT, 'Sklad A', 'Horna', 1, 'Brno', 44444, 5200)
    RETURNING ic INTO sklad_a_ic;
    INSERT INTO budova VALUES (DEFAULT, 'Sklad B', 'Horna', 2, 'Brno', 44444, 7800)
    RETURNING ic INTO sklad_b_ic;

    INSERT INTO dodavatel VALUES (DEFAULT, 'Madrigal', 'Dolna', 89, 'Frydek-Mistek', 22255, '+420481231234')
    RETURNING id INTO madrigal_id;

    INSERT INTO krajina_povodu VALUES (DEFAULT, 'Rakusko', 'Europa', 'mierne')
    RETURNING ic INTO rakusko_ic;
    INSERT INTO krajina_povodu VALUES (DEFAULT, 'Svajciarsko', 'Europa', 'mierne')
    RETURNING ic INTO svajciarsko_ic;

    INSERT INTO druh_syra VALUES (DEFAULT, 'gouda', 'krava', 15, DEFAULT, rakusko_ic)
    RETURNING ic INTO gouda_ic;
    INSERT INTO druh_syra VALUES (DEFAULT, 'ostiepok', 'krava', 15, 30, svajciarsko_ic)
    RETURNING ic INTO ostiepok_ic;
    INSERT INTO druh_syra VALUES (DEFAULT, 'gouda2', 'krava', 15, DEFAULT, rakusko_ic)
    RETURNING ic INTO gouda2_ic;
    INSERT INTO druh_syra VALUES (DEFAULT, 'ostiepok2', 'krava', 15, 30, svajciarsko_ic)
    RETURNING ic INTO ostiepok2_ic;

    INSERT INTO objednavka VALUES (DEFAULT, 'dorucena', TO_DATE('25.03.2021','DD.MM.YYYY'), 19.50, gus_id, madrigal_id)
    RETURNING ic INTO objednavka_1_ic;
    INSERT INTO objednavka VALUES (DEFAULT, 'odoslana', TO_DATE('03.04.2021','DD.MM.YYYY'), 1450, gus_id, madrigal_id)
    RETURNING ic INTO objednavka_2_ic;

    INSERT INTO druh_syra_v_objednavke VALUES (objednavka_1_ic, gouda_ic, 10);
    INSERT INTO druh_syra_v_objednavke VALUES (objednavka_2_ic, gouda_ic, 180);
    INSERT INTO druh_syra_v_objednavke VALUES (objednavka_2_ic, ostiepok_ic, 130);

    INSERT INTO bochnik VALUES (DEFAULT, 6, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('20.03.2022','DD.MM.YYYY'), gouda_ic, sklad_a_ic, madrigal_id)
    RETURNING ic INTO bochnik_1_ic;
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda2_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda2_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok2_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok2_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda2_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda2_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok2_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok2_ic, sklad_a_ic, madrigal_id);

    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda2_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda2_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok2_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok2_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda2_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda2_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok2_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok2_ic, sklad_a_ic, madrigal_id);

    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda2_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda2_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok2_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok2_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda2_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda2_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok2_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok2_ic, sklad_a_ic, madrigal_id);

    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda2_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda2_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok2_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok2_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda2_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda2_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok2_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok2_ic, sklad_a_ic, madrigal_id);

    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda2_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda2_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok2_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok2_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda2_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda2_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok2_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok2_ic, sklad_a_ic, madrigal_id);

    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda2_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda2_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok2_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok2_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda2_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), gouda2_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok2_ic, sklad_a_ic, madrigal_id);
    INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), ostiepok2_ic, sklad_a_ic, madrigal_id);


    INSERT INTO presun_tovaru VALUES (DEFAULT, 'vytvorena', TO_DATE('03.04.2021','DD.MM.YYYY'), 1, gus_id, DEFAULT, sklad_a_ic, sklad_b_ic)
    RETURNING ic INTO presun_1_ic;

    INSERT INTO presun_bochnika VALUES (presun_1_ic, bochnik_1_ic);

    COMMIT;
END;
/


-------------------------------------------------------------------------------------------------------------
-- EXEMPLARY PROCEDURE EXECUTION

BEGIN CHEESE_TYPE_IN_ORDERS('gouda'); END;
BEGIN CHEESE_TYPE_IN_ORDERS('emental'); END;
BEGIN PERCENTAGE_OF_CHEESE_TYPE('ostiepok'); END;
BEGIN PERCENTAGE_OF_CHEESE_TYPE('gouda'); END;


-------------------------------------------------------------------------------------------------------------
-- EXEMPLARY DATA SELECTION

--zamestnanci, ktorý vykonali objednávku s hodnotou nad 1000€
SELECT DISTINCT Z.*, O.* FROM ZAMESTNANEC Z, OBJEDNAVKA O
WHERE Z.id=O.zamestnanec_fk AND O.suma>1000;
/

--bochníky od Madrigal
SELECT * FROM BOCHNIK B, DODAVATEL D
WHERE B.dodavatel_fk = D.id AND D.nazov = 'Madrigal'
ORDER BY B.ic;
/

--všetky žiadosti o presun tovaru do budovy Sklad B
SELECT DISTINCT Z.* FROM PRESUN_BOCHNIKA Z, PRESUN_TOVARU P, BUDOVA B
WHERE Z.PRESUN_FK = P.IC AND P.PRESUN_DO_FK = B.IC AND B.MENO='Sklad B'
ORDER BY Z.PRESUN_FK;
/

--počet bochníkov pre jednotlivé druhy syra
SELECT D.meno, COUNT(B.IC) FROM DRUH_SYRA D, BOCHNIK B
WHERE B.DRUH_SYRA_FK=D.IC
GROUP BY D.meno;
/

--celková hodnota objednávok jednotlivých dodávateľov
SELECT D.NAZOV, SUM(SUMA) FROM DODAVATEL D, OBJEDNAVKA O
WHERE O.DODAVATEL_FK=D.ID
GROUP BY D.NAZOV;
/

--druhy syrov ktoré sa nachádzajú iba v budove Sklad A
SELECT DISTINCT D.* FROM DRUH_SYRA D, BUDOVA B, BOCHNIK BO
WHERE BO.DRUH_SYRA_FK = D.IC AND BO.BUDOVA_FK = B.IC AND B.MENO = 'Sklad A'
AND NOT EXISTS(SELECT D.* FROM DRUH_SYRA D, BUDOVA B, BOCHNIK BO
WHERE BO.DRUH_SYRA_FK = D.IC AND BO.BUDOVA_FK = B.IC AND B.MENO <> 'Sklad A');
/

--zamestnanci ktorý doručili nejakú objednávku
SELECT * FROM ZAMESTNANEC Z
WHERE Z.ID IN (SELECT O.ZAMESTNANEC_FK FROM OBJEDNAVKA O WHERE O.STAV = 'dorucena');
/


-------------------------------------------------------------------------------------------------------------
-- EXPLAIN PLAN not using and using INDEX

EXPLAIN PLAN FOR
SELECT druh_syra.meno, COUNT(bochnik.druh_syra_fk) FROM druh_syra
INNER JOIN bochnik on druh_syra.ic = bochnik.druh_syra_fk
WHERE krajina_povodu_fk = 2
GROUP BY druh_syra.meno;

-- explain plan bez indexu
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);


CREATE INDEX bochnik_podla_druhu ON bochnik (druh_syra_fk);

EXPLAIN PLAN FOR
SELECT druh_syra.meno, COUNT(bochnik.druh_syra_fk) FROM druh_syra
INNER JOIN bochnik on druh_syra.ic = bochnik.druh_syra_fk
WHERE krajina_povodu_fk = 2
GROUP BY druh_syra.meno;

-- explain plan s indexom
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);

-------------------------------------------------------------------------------------------------------------
-- PRIVILEGES

GRANT ALL ON zamestnanec TO XKLUCI01;
GRANT ALL ON dodavatel TO XKLUCI01;
GRANT ALL ON objednavka TO XKLUCI01;
GRANT ALL ON presun_tovaru TO XKLUCI01;
GRANT ALL ON budova TO XKLUCI01;
GRANT ALL ON krajina_povodu TO XKLUCI01;
GRANT ALL ON druh_syra TO XKLUCI01;
GRANT ALL ON bochnik TO XKLUCI01;
GRANT ALL ON druh_syra_v_objednavke TO XKLUCI01;
GRANT ALL ON nadradeny_zamestnanec TO XKLUCI01;
GRANT ALL ON presun_bochnika TO XKLUCI01;

GRANT EXECUTE ON DROP_IF_EXISTS TO XKLUCI01;
GRANT EXECUTE ON CHEESE_TYPE_IN_ORDERS TO XKLUCI01;
GRANT EXECUTE ON PERCENTAGE_OF_CHEESE_TYPE TO XKLUCI01;

-- pokus o udelenie prav na vytvorenie materializovaneho pohladu pre kolegu, neuspesny z dovodu nedostatocnych prav
-- GRANT CREATE ANY MATERIALIZED VIEW TO XKLUCI01;
-- GRANT CREATE ANY TABLE TO XKLUCI01;


-------------------------------------------------------------------------------------------------------------
-- MATERIALIZED VIEW

BEGIN
    EXECUTE IMMEDIATE 'DROP MATERIALIZED VIEW materialized_view';
EXCEPTION WHEN OTHERS THEN
    IF SQLCODE != -12003 THEN
        RAISE;
    END IF;
END;

--CREATE MATERIALIZED VIEW XKLUCI01.materialized_view AS
CREATE MATERIALIZED VIEW materialized_view AS
SELECT druh_syra.meno, COUNT(bochnik.druh_syra_fk) FROM druh_syra
INNER JOIN bochnik on druh_syra.ic = bochnik.druh_syra_fk
GROUP BY druh_syra.meno;


-------------------------------------------------------------------------------------------------------------
-- MATERIALIZED VIEW DEMONSTRATION

-- content of materialized view does not change when the original table does (it needs to refreshed)
-- materialized view pred insertom
SELECT * from materialized_view;
INSERT INTO bochnik VALUES (DEFAULT, 5.5, 5, TO_DATE('01.04.2021','DD.MM.YYYY'), TO_DATE('21.03.2022','DD.MM.YYYY'), 2, 1, 1);
COMMIT;
-- materialized view po inserte
SELECT * from materialized_view;