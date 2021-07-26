-- Table: public.indicators_raw

DROP TABLE public.indicators_raw;

CREATE TABLE public.indicators_raw
(
    papel character varying(10) COLLATE pg_catalog."default" NOT NULL,
    tipo character varying(10) COLLATE pg_catalog."default",
    empresa character varying(120) COLLATE pg_catalog."default",
    setor character varying(80) COLLATE pg_catalog."default",
    subsetor character varying(80) COLLATE pg_catalog."default",
    data_ult_cot date,
    min_52_sem double precision,
    max_52_sem double precision,
    vol_med_2m double precision,
    valor_da_firma double precision,
    nro_acoes double precision,
    "dia%" double precision,
    "mes%" double precision,
    "var_30_dias%" double precision,
    "var_12_meses%" double precision,
    "var_2021%" double precision,
    "var_2020%" double precision,
    "var_2019%" double precision,
    "var_2018%" double precision,
    "var_2017%" double precision,
    "var_2016%" double precision,
	"var_2015%" double precision,
    "var_2014%" double precision,
    p_l double precision,
    p_vp double precision,
    p_ebit double precision,
    psr double precision,
    p_ativos double precision,
    p_cap_giro double precision,
    p_ativ_circ_liq double precision,
    "div_yield%" double precision,
    ev_ebitda double precision,
    ev_ebit double precision,
    "cres_rec_5a%" double precision,
    lpa double precision,
    vpa double precision,
    "marg_bruta%" double precision,
    "marg_ebit%" double precision,
    "marg_liquida%" double precision,
    "ebit_ativo%" double precision,
    "roic%" double precision,
    "roe%" double precision,
    liquidez_corr double precision,
    div_br_patrim double precision,
    giro_ativos double precision,
    ativo double precision,
    disponibilidades double precision,
    ativo_circulante double precision,
    div_bruta double precision,
    div_liquida double precision,
    patrim_liq double precision,
    cotacao double precision,
    receita_liquida_ult_12_mes double precision,
    receita_liquida_ult_3_mes double precision,
    ebit_ult_12_mes double precision,
    ebit_ult_3_mes double precision,
    lucro_liquido_ult_12_mes double precision,
    lucro_liquido_ult_3_mes double precision,
	carteira_de_credito double precision,
    depositos double precision,
	resultado_intermed_financ_ult_12_mes double precision,
	resultado_intermed_financ_ult_3_mes double precision,
	receita_servicos_ult_12_mes double precision,
	receita_servicos_ult_3_mes double precision
)

TABLESPACE pg_default;

ALTER TABLE public.indicators_raw
    OWNER to postgres;

GRANT INSERT, SELECT, UPDATE, DELETE, TRUNCATE ON TABLE public.indicators_raw TO myuser;

GRANT ALL ON TABLE public.indicators_raw TO postgres;