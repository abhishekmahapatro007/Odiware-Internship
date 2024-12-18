# Odoo Source Installation Guide

The source “installation” is not about installing Odoo but running it directly from the source instead.

Using the Odoo source is ideal for module developers as it offers greater accessibility compared to packaged installers. This approach provides flexibility and control, allowing for explicit starting and stopping of Odoo, overriding settings via command-line parameters, and maintaining multiple Odoo versions side-by-side.

---

## Fetching the Source Code

### 1. *Archive*
#### Community Edition:
- [Odoo Download Page](https://www.odoo.com/page/download)
- [GitHub Community Repository](https://github.com/odoo/odoo)
- [Nightly Server](http://nightly.odoo.com/)

#### Enterprise Edition:
- [Odoo Download Page](https://www.odoo.com/page/download)
- [GitHub Enterprise Repository](https://github.com/odoo/enterprise)

### 2. *Git*
#### Prerequisite:
- Install Git and ensure basic knowledge of Git commands.

#### Cloning Options:
1. *Clone with HTTPS*
   bash
   git clone https://github.com/odoo/odoo.git
   git clone https://github.com/odoo/enterprise.git

For more detailed information, please refer to the [official Odoo documentation](https://www.odoo.com/documentation/18.0/administration/on_premise/source.html).

# Odoo 17.0 Installation and Setup Guide Step-by-Step

## Prerequisites
1. Install PostgreSQL 15 and python 3.10.
2. Create a new user with login role:


---

## Git Setup

### Step 1: Clone the Odoo Repository
Run the following command in your terminal:
```ini
git clone https://github.com/odoo/odoo.git --branch 17.0 --single-branch --depth 1
```

### Step 2: Download Git
Ensure Git is installed on your system before proceeding.

---

## Setting Up Odoo Files

### Step 1: Open Odoo Directory in File Explorer
Run the following command in your terminal:
explorer .


### Step 2: Move Odoo Folder
Move the Odoo folder into your `Documents` directory.

### Step 3: Create `odoo.conf` File
1. Inside the Odoo folder, create a text document named `odoo.conf`.
2. Rename `odoo.conf.text` to `odoo.conf`.
3. Add the following configuration to the `odoo.conf` file:
```ini
[options]
addons_path = ./addons
admin_passwd = admin
csv_internal_sep = ,
data_dir = c:\users\pc\appdata\local\openerp s.a\odoo
db_host = False
db_maxconn = 64
db_maxconn_gevent = False
db_name = odoo_db
db_password = admin
db_port = False
db_sslmode = prefer
db_template = template0
db_user = odoo
dbfilter = 
demo = {'base': 1}
email_from = False
from_filter = False
geoip_city_db = c:\usr\share\geoip\geolite2-city.mmdb
geoip_country_db = c:\usr\share\geoip\geolite2-country.mmdb
gevent_port = 8072
http_enable = True
http_interface = 
http_port = 8069
import_partial = 
limit_memory_hard = None
limit_memory_soft = None
limit_request = None
limit_time_cpu = None
limit_time_real = None
limit_time_real_cron = None
list_db = True
log_db = False
log_db_level = warning
log_handler = :INFO
log_level = info
logfile = 
max_cron_threads = 2
osv_memory_count_limit = 0
pg_path = 
pidfile = 
proxy_mode = False
reportgz = False
screencasts = 
screenshots = c:\users\pc\appdata\local\temp\odoo_tests
server_wide_modules = base,web
smtp_password = False
smtp_port = 25
smtp_server = localhost
smtp_ssl = False
smtp_ssl_certificate_filename = False
smtp_ssl_private_key_filename = False
smtp_user = False
syslog = False
test_enable = False
test_file = 
test_tags = None
transient_age_limit = 1.0
translate_modules = ['all']
unaccent = False
upgrade_path = 
websocket_keep_alive_timeout = 3600
websocket_rate_limit_burst = 10
websocket_rate_limit_delay = 0.2
without_demo = False
workers = None
x_sendfile = False
```

---

## VS Code Setup

### Step 1: Navigate to Odoo Directory
Type cmd in the path bar and open command prompt,then use code . to open vs code in the designated directory


---

## Virtual Environment Setup

### Step 1: Create a Virtual Environment
1. Open the Odoo directory.
2. Right-click and open the terminal in this directory as admin.
3. Run the following command:
```ini
py -m venv .venv
```
(if running for the first time,else skip it)


### Step 2: Activate Virtual Environment
Run the appropriate activation command:
```ini
.venv\Scripts\activate
```
---

## Resources

- [Odoo Repository](https://github.com/odoo/odoo)
- [odoo.conf file download](https://odiwaretech-my.sharepoint.com/personal/kunal_rout_odiware_com/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fkunal%5Frout%5Fodiware%5Fcom%2FDocuments%2FMicrosoft%20Teams%20Chat%20Files%2Fodoo%20%281%29%2Econf&parent=%2Fpersonal%2Fkunal%5Frout%5Fodiware%5Fcom%2FDocuments%2FMicrosoft%20Teams%20Chat%20Files&ga=1)
