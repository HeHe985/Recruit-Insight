CREATE TABLE job_postings_jobpostinglist (
    emp_seqno INT PRIMARY KEY,
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

CREATE TABLE accounts_bookmark (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    job_posting_id INT NOT NULL,
    CONSTRAINT fk_bookmark_user
        FOREIGN KEY (user_id) REFERENCES auth_user(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_bookmark_job
        FOREIGN KEY (job_posting_id) REFERENCES job_postings_jobpostinglist(emp_seqno)
        ON DELETE CASCADE,
    UNIQUE KEY unique_user_job (user_id, job_posting_id)
);

CREATE TABLE job_postings_jobpostingdetail (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    emp_seqno_id INT NOT NULL,
    emp_recr_nm VARCHAR(100) NOT NULL,
    job_cont TEXT NOT NULL,
    emp_wanted_career_nm VARCHAR(100),
    emp_wanted_edu_nm VARCHAR(100),
    spt_cert_etc TEXT,
    recr_psncnt INT,
    emp_recr_memo_cont TEXT,
    work_region_nm VARCHAR(100),
    CONSTRAINT fk_detail_job
        FOREIGN KEY (emp_seqno_id)
        REFERENCES job_postings_jobpostinglist(emp_seqno)
        ON DELETE CASCADE
);

CREATE TABLE job_postings_occupationtype (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    emp_seqno_id INT NOT NULL,
    jobs_cd VARCHAR(100) NOT NULL,
    jobs_cd_kor_nm VARCHAR(100),
    CONSTRAINT fk_occupation_job
        FOREIGN KEY (emp_seqno_id)
        REFERENCES job_postings_jobpostinglist(emp_seqno)
        ON DELETE CASCADE
);

CREATE TABLE financial_statement_corpcode (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    corp_code VARCHAR(8) UNIQUE NOT NULL,
    corp_name VARCHAR(50) NOT NULL,
    corp_eng_name VARCHAR(100),
    stock_code VARCHAR(6),
    modify_date VARCHAR(8),
    INDEX idx_corp_name (corp_name)
);

CREATE TABLE financial_statement_sjdiv (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    sj_div VARCHAR(5) UNIQUE NOT NULL,
    sj_nm VARCHAR(5) NOT NULL
);

CREATE TABLE financial_statement_financialdata (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    corp_code_id BIGINT NOT NULL,
    bsns_year INT NOT NULL,
    account_id VARCHAR(50) NOT NULL,
    account_nm VARCHAR(50) NOT NULL,
    account_detail VARCHAR(50) NOT NULL,
    reprt_code VARCHAR(5) NOT NULL,
    sj_div_id BIGINT NOT NULL,
    thstrm_nm VARCHAR(10),
    thstrm_amount DECIMAL(25,5),
    currency VARCHAR(5),
    CONSTRAINT fk_fd_corp
        FOREIGN KEY (corp_code_id)
        REFERENCES financial_statement_corpcode(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_fd_sj
        FOREIGN KEY (sj_div_id)
        REFERENCES financial_statement_sjdiv(id)
        ON DELETE CASCADE,
    CONSTRAINT unique_corp_bsns_account
        UNIQUE (corp_code_id, bsns_year, account_id, account_detail)
);

CREATE TABLE financial_statement_financialratio (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    corp_code_id BIGINT NOT NULL,
    bsns_year INT NOT NULL,
    ratio_id VARCHAR(50) NOT NULL,
    ratio_nm VARCHAR(50) NOT NULL,
    reprt_code VARCHAR(5) NOT NULL,
    category VARCHAR(10) NOT NULL,
    thstrm_nm VARCHAR(10),
    thstrm_amount DECIMAL(20,7),
    unit VARCHAR(5),
    CONSTRAINT fk_fr_corp
        FOREIGN KEY (corp_code_id)
        REFERENCES financial_statement_corpcode(id)
        ON DELETE CASCADE,
    CONSTRAINT unique_corp_bsns_ratio
        UNIQUE (corp_code_id, bsns_year, ratio_id)
);

CREATE TABLE accounts_recommendation (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    job_id INT NOT NULL,
    score INT DEFAULT 0,
    reason TEXT NOT NULL,
    CONSTRAINT fk_rec_user
        FOREIGN KEY (user_id)
        REFERENCES auth_user(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_rec_job
        FOREIGN KEY (job_id)
        REFERENCES job_postings_jobpostinglist(emp_seqno)
        ON DELETE CASCADE,
    UNIQUE KEY unique_user_job (user_id, job_id)
);

CREATE TABLE cover_letter (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,

    user_id BIGINT NOT NULL,
    question VARCHAR(100) NOT NULL,
    category CHAR(1) NOT NULL,
    content TEXT NOT NULL,
    note TEXT NOT NULL,

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_cover_letter_user
        FOREIGN KEY (user_id)
        REFERENCES user (id)
        ON DELETE CASCADE
);

ALTER TABLE cover_letter
ADD CONSTRAINT chk_cover_letter_category
CHECK (category IN ('1','2','3','4','5','6','7','8','9'));

CREATE TABLE auth_user (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,

    password VARCHAR(128) NOT NULL,
    last_login DATETIME NULL,

    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    username VARCHAR(150) NOT NULL UNIQUE,
    first_name VARCHAR(150) NOT NULL DEFAULT '',
    last_name VARCHAR(150) NOT NULL DEFAULT '',
    email VARCHAR(254) NOT NULL DEFAULT '',

    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    date_joined DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
