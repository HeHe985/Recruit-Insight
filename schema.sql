CREATE TABLE job_postings_jobpostinglist (
    emp_seqno INTEGER PRIMARY KEY,
    emp_wanted_title VARCHAR(200) NOT NULL,
    emp_busi_nm VARCHAR(100) NOT NULL,
    co_clcd_nm VARCHAR(100),
    emp_wanted_stdt DATE NOT NULL,
    emp_wanted_endt DATE NOT NULL,
    emp_wanted_type_nm VARCHAR(200) NOT NULL,
    reg_log_img_nm TEXT NOT NULL,
    emp_wanted_homepg_detail TEXT NOT NULL,
    emp_wanted_mobile_url TEXT,
    emp_wanted_homepg TEXT,
    empn_recr_summary_cont TEXT,
    recr_comm_cont TEXT,
    emp_submit_doc_cont TEXT,
    emp_rcpt_mthd_cont TEXT,
    emp_acpt_psn_annc_cont DATE,
    inqry_cont TEXT,
    empn_etc_cont TEXT,
    recruitment_process TEXT
);


CREATE TABLE job_postings_occupationtype (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    emp_seqno INTEGER NOT NULL,
    jobs_cd VARCHAR(100) NOT NULL,
    jobs_cd_kor_nm VARCHAR(100),

    CONSTRAINT fk_occupation_emp
        FOREIGN KEY (emp_seqno)
        REFERENCES job_postings_jobpostinglist (emp_seqno)
        ON DELETE CASCADE
);


CREATE TABLE job_postings_jobpostingdetail (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    emp_seqno INTEGER NOT NULL,
    emp_recr_nm VARCHAR(100) NOT NULL,
    job_cont TEXT NOT NULL,
    emp_wanted_career_nm VARCHAR(100),
    emp_wanted_edu_nm VARCHAR(100),
    spt_cert_etc TEXT,
    recr_psncnt INTEGER,
    emp_recr_memo_cont TEXT,
    work_region_nm VARCHAR(100),

    CONSTRAINT fk_detail_emp
        FOREIGN KEY (emp_seqno)
        REFERENCES job_postings_jobpostinglist (emp_seqno)
        ON DELETE CASCADE
);

-- DART
CREATE TABLE corp_code (
    id SERIAL PRIMARY KEY,
    corp_code VARCHAR(8) NOT NULL UNIQUE,
    corp_name VARCHAR(50) NOT NULL
);

CREATE INDEX idx_corp_code_corp_name ON corp_code(corp_name);

CREATE TABLE sj_div (
    id SERIAL PRIMARY KEY,
    sj_div VARCHAR(5) NOT NULL UNIQUE,
    sj_nm VARCHAR(5) NOT NULL
);

CREATE TABLE financial_data (
    id SERIAL PRIMARY KEY,
    corp_code INTEGER NOT NULL,
    bsns_year INTEGER NOT NULL,
    account_id VARCHAR(50) NOT NULL,
    account_nm VARCHAR(50) NOT NULL,
    account_detail VARCHAR(50) NOT NULL,
    reprt_code VARCHAR(5) NOT NULL,
    sj_div INTEGER NOT NULL,
    thstrm_nm VARCHAR(10),
    thstrm_amount DECIMAL(25, 5),
    currency VARCHAR(5) NOT NULL,
    CONSTRAINT fk_financial_data_corp FOREIGN KEY (corp_code) REFERENCES corp_code (id) ON DELETE CASCADE,
    CONSTRAINT fk_financial_data_sj FOREIGN KEY (sj_div) REFERENCES sj_div (id) ON DELETE CASCADE,
    CONSTRAINT corp_bsns_account UNIQUE (corp_code, bsns_year, account_id, account_detail)
);

CREATE TABLE financial_ratio (
    id SERIAL PRIMARY KEY,
    corp_code INTEGER NOT NULL,
    bsns_year INTEGER NOT NULL,
    ratio_id VARCHAR(50) NOT NULL,
    ratio_nm VARCHAR(50) NOT NULL,
    reprt_code VARCHAR(5) NOT NULL,
    category VARCHAR(10) NOT NULL,
    thstrm_nm VARCHAR(10),
    thstrm_amount DECIMAL(20, 7),
    unit VARCHAR(5) NOT NULL,
    CONSTRAINT fk_financial_ratio_corp FOREIGN KEY (corp_code) REFERENCES corp_code (id) ON DELETE CASCADE,
    CONSTRAINT corp_bsns_ratio UNIQUE (corp_code, bsns_year, ratio_id)
);