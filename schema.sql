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
