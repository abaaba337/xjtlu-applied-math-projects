# 数据与中间产物

路径相对于 `COVID_DATA_DIR`（默认本目录）。当前包含分析代码，未包含下列外部数据。不要以空停用词或虚构数据代替研究输入。

## 主要外部输入

| 目录 | 文件 | 用途与关键字段 |
| --- | --- | --- |
| `tweets/` | `Copy of Copy of Coronavirus [EN] [Scaled x4] [Pittsburgh].csv` | T1 跳过前六行读取；`Date`、`Domain`、`Title`、`Full Text` |
| `tweets/` | `stopwords_en.txt`、`extra_stopwords_en.txt` | 每行一个停用词，清洗过程可能更新扩展列表 |
| `national-news/` | `covid-news-en-us-clean-keyonly.csv` | `Date`、`keyword`、`scopes`；当前从已整理表开始，原始转换代码保留作研究记录 |
| `national-news/` | `stopwords_en.txt`、`extra_stopwords_en.txt` | 独立的新闻关键词停用词 |
| `news/` | `cbs_Pittsburgh.csv` | `Date`、`Title`、`Keywords`、`Content` |
| `news/` | `stopwords_en.txt`、`stopwords_html.txt`、`stopwords_punctuation.txt` | 新闻清洗规则 |
| `mobility/Delta TSPP/` | `DTSPP_US_Mobility_formalized.csv` | `fips`、`date`、`dtspp` 和探索所用行政区字段 |
| `mobility/Google/` | `Google_US_Mobility_formalized.csv` | Google 已格式化出行指标 |
| `mobility/Descartes Labs/` | `DL_US_Mobility_formalized.csv` | `fips`、`date`、`m50`、`m50_pct_change` 和行政区字段 |
| `mobility/Facebook/` | `Facebook_US_Mobility_formalized.csv` | Facebook 已格式化出行指标 |
| `mobility/Gov/` | `Gov_US_Mobility_formalized.csv` | 政府已格式化出行指标 |
| `mobility/Policy/Chicago/` | `Local-Policy-Responses-formalized.csv` | M2 政策探索输入 |
| `mobility/` | `Local-Policy-Responses-formalized-matched-localonly.csv` | M3 的已匹配政策表；FIPS、州县、居家/营业/餐厅政策起止日期；M2 不自动完成此表的全部预处理 |
| `mobility/` | `matched-us-covidcase-counties-2020.csv` | `fips`、`date`、`cases`、`deaths`、`new_cases`、`new_deaths` |
| `mobility/trends/` | `google-trends-locations.json`、`google-trend-geocode2metro.csv`、`county-msa-csa.csv` | 地理代码与名称；匹配使用 `metro`、`MSA Title` 等字段 |

`python project_paths.py` 检查这些主要文件是否存在，不验证全部字段、模型或在线资源。县级 FIPS 保留五位，匹配键为 `(fips, date)`，重复键须先调查。

## 生成与消费关系

- **T1 → T2，`tweets/`**：T1 生成 `tw_pitt_cleaned.csv`、`tw_pitt_cleaned_onlytext.csv`、`tw_pitt_original_cleaned.csv`；T2 读取 `Doc1_text2day.csv`、`Doc2_VN2day.csv`、`Doc3_N2day.csv`、`Doc4_original_text2day.csv`、`Doc5_original_VN2day.csv`、`Doc6_original_N2day.csv`，写出 TF-IDF CSV 与 `plot/` 图片。
- **N1，`national-news/`**：输出 `Doc1_key2day.csv`、`Doc2_key_VN2day.csv`、`Doc3_key_N2day.csv`，不自动接入地方新闻路线。
- **N2 → N3，`news/Data/CBS_KDKA/`**：N2 生成清洗表、四组日文档、`TFIDF/` 词权重、`LDA/` 模型与主题占比。N3 使用同批次的 `adjusted_LDA*.pkl`；先检查 N2 的训练与保存开关，不能只执行载入模型部分。
- **M1，`mobility/trends/`**：生成 `google-trend-Coronavirus_disease_2019_byday.csv`、`..._byregion.csv` 及 `_sorted.csv`。缺失地区不能当成零关注度。
- **M2，`mobility/trends/`**：人工检查匹配后生成 `googel-trend-metro2county-clean-version.csv`，上下游保留该拼写。
- **M3 → M4，`mobility/`**：生成 `combined_info.csv`；连接 Descartes Labs 指标后生成 `combined_info_with_dl.csv`。未匹配到的指标保留缺失值，不插入零。

输入与产出默认被 Git 忽略。独立保存数据副本及来源、获取日期、字段定义和许可；只载入可信的序列化模型。
