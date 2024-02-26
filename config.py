TOKEN = ''
ADMINS = (5344024150, )
API_ID = 
API_HASH = "" 

MYSQL_PASSWORD = 'password'
MYSQL_USER = 'root'
MYSQL_DATABASE = 'virustotal'

TEXTS = {
    'start': {
        'ru': '''Привет. Функционал этого бота реализован через API VirusTotal, что позволяет ему проверять файлы, ссылки и IP-адреса с помощью 70 антивирусов одновременно. Просто отправьте сюда данные, и Вы получите подробный отчет о наличии вирусов и угроз.

Бот является полностью бесплатным. Вы не увидите тут рекламу, спам или платные функции. Если у Вас есть желание поддержать этот проект, то самым большим вкладом будет подписка на наши каналы: <a href="https://t.me/+Z4wrctbz7m40MTEy">Infosec</a> и <a href="https://t.me/+q3a-KS46N4owZGQy">ZeroDay</a> (но это не обязательно), а контакты и возможность донатов есть на вкладке "информация". Всем безопасности!''',

        'eng': '''Hello. The functionality of this bot is implemented through the VirusTotal API, which allows it to check files, links, and IP addresses using 70 antiviruses simultaneously. Just send the data here, and you will receive a detailed report on the presence of viruses and threats.

The bot is completely free. You won't see any advertisements, spam, or paid features here. If you have the desire to support this project, the biggest contribution would be subscribing to our channels: <a href="https://t.me/+Z4wrctbz7m40MTEy">Infosec</a> and <a href="https://t.me/+q3a-KS46N4owZGQy">ZeroDay</a> (but it's optional), and contact information and donation options are available on the "Information" tab. Stay safe, everyone!''',

        'ukr': '''Привіт. Функціонал цього бота реалізовано через API VirusTotal, що дозволяє йому перевіряти файли, посилання та IP-адреси за допомогою 70 антивірусів одночасно. Просто надішліть сюди дані, і ви отримаєте детальний звіт про наявність вірусів та загроз.

Бот повністю безкоштовний. Тут ви не побачите рекламу, спам або платні функції. Якщо у вас є бажання підтримати цей проект, то найбільшим внеском буде підписка на наші канали: <a href="https://t.me/+Z4wrctbz7m40MTEy">Infosec</a> та <a href="https://t.me/+q3a-KS46N4owZGQy">ZeroDay</a> (але це не обов'язково), а контакти та можливість пожертвувань є на вкладці "інформація". Всім безпеки!''',

        'deut': '''Hallo. Die Funktionalität dieses Bots wird über die VirusTotal-API implementiert, was es ihm ermöglicht, Dateien, Links und IP-Adressen gleichzeitig mit 70 Antivirenprogrammen zu überprüfen. Senden Sie einfach die Daten hierhin, und Sie erhalten einen detaillierten Bericht über das Vorhandensein von Viren und Bedrohungen.

Der Bot ist komplett kostenlos. Hier werden Sie keine Werbung, Spam oder kostenpflichtige Funktionen sehen. Wenn Sie dieses Projekt unterstützen möchten, wäre das größte Engagement das Abonnieren unserer Kanäle: <a href="https://t.me/+Z4wrctbz7m40MTEy">Infosec</a> und <a href="https://t.me/+q3a-KS46N4owZGQy">ZeroDay</a> (aber dies ist optional), und Kontaktdaten und Spendenmöglichkeiten finden Sie im "Informationen" Tab. Bleiben Sie sicher, alle zusammen!''',

        'esp': '''Hola. La funcionalidad de este bot se implementa a través de la API de VirusTotal, lo que le permite verificar archivos, enlaces y direcciones IP utilizando 70 antivirus al mismo tiempo. Simplemente envía los datos aquí y recibirás un informe detallado sobre la presencia de virus y amenazas.

El bot es completamente gratuito. No verás anuncios, spam ni funciones de pago aquí. Si deseas apoyar este proyecto, la mayor contribución sería suscribirte a nuestros canales: <a href="https://t.me/+Z4wrctbz7m40MTEy">Infosec</a> y <a href="https://t.me/+q3a-KS46N4owZGQy">ZeroDay</a> (pero no es obligatorio). Los contactos y las opciones de donación están disponibles en la pestaña "Información". ¡Manténte seguro/a!''',

        'fren': '''Bonjour. La fonctionnalité de ce bot est mise en œuvre via l'API VirusTotal, ce qui lui permet de vérifier les fichiers, les liens et les adresses IP à l'aide de 70 antivirus simultanément. Il vous suffit d'envoyer les données ici et vous recevrez un rapport détaillé sur la présence de virus et de menaces.

Le bot est entièrement gratuit. Vous ne verrez pas de publicités, de spam ou de fonctionnalités payantes ici. Si vous souhaitez soutenir ce projet, la plus grande contribution serait de vous abonner à nos chaînes : <a href="https://t.me/+Z4wrctbz7m40MTEy">Infosec</a> et <a href="https://t.me/+q3a-KS46N4owZGQy">ZeroDay</a> (mais ce n'est pas obligatoire), et les contacts et les options de don sont disponibles dans l'onglet "Information". Restez en sécurité !''',

        'ital': '''Ciao. La funzionalità di questo bot è implementata tramite l'API di VirusTotal, che gli consente di controllare file, link e indirizzi IP utilizzando contemporaneamente 70 antivirus. Basta inviare i dati qui e riceverai un rapporto dettagliato sulla presenza di virus e minacce.

Il bot è completamente gratuito. Qui non vedrai pubblicità, spam o funzioni a pagamento. Se desideri sostenere questo progetto, il contributo più grande sarebbe abbonarsi ai nostri canali: <a href="https://t.me/+Z4wrctbz7m40MTEy">Infosec</a> e <a href="https://t.me/+q3a-KS46N4owZGQy">ZeroDay</a> (ma non è obbligatorio) e le informazioni di contatto e le opzioni di donazione sono disponibili nella scheda "Informazioni". Rimanete al sicuro!'''

    },
    'settings': {
        'ru': 'Выбери какие типы данных будут сканироваться',
        'eng': 'Choose which data types to scan',
        'ukr': 'Вибери, які типи даних слід сканувати',
        'deut': 'Wähle aus, welche Datenarten gescannt werden sollen',
        'esp': 'Elige qué tipos de datos escanear',
        'fren': 'Choisissez quels types de données scanner',
        'ital': 'Scegli quali tipi di dati scansionare'
    },

    'lang_btn': {
        'ru': '🇷🇺Язык',
        'eng': '🇬🇧Language',
        'ukr': '🇺🇦Мова',
        'deut': '🇩🇪Sprache',
        'esp': '🇪🇸Idioma',
        'fren': '🇫🇷Langue',
        'ital': '🇮🇹Lingua'
    },
    'add_chat_btn': {
        'ru': 'Добавить бота в чат',
        'eng': 'Add a bot to a chat',
        'ukr': 'Додайте бота до чату',
        'deut': 'Fügen Sie einem Chat einen Bot hinzu',
        'esp': 'Agrega un bot a un chat',
        'fren': 'Ajouter un bot à une conversation',
        'ital': 'Aggiungi un bot a una chat'
    },
    'info_btn': {
        'ru': 'Информация',
        'eng': 'Information',
        'ukr': 'Інформація',
        'deut': 'Information',
        'esp': 'Información',
        'fren': 'Information',
        'ital': 'Informazione'
    },
    'settings_btn': {
        'ru': 'Настройки сканирования',
        'eng': 'Scan Settings',
        'ukr': 'Налаштування сканування',
        'deut': 'Scan-Einstellungen',
        'esp': 'Configuración de escaneo',
        'fren': 'Paramètres de numérisation',
        'ital': 'Impostazioni di scansione'
    },
    'back_btn': {
        'ru': 'Назад',
        'eng': 'Back',
        'ukr': 'Back',
        'deut': 'Basack',
        'esp': 'Baack',
        'fren': 'Back',
        'ital': 'Bacrk'
    },

    'settings_menu': {
        'file': {
            'ru': 'Файлы',
            'eng': 'Files',
            'ukr': 'Файли',
            'deut': 'Dateien',
            'esp': 'Archivos',
            'fren': 'Fichiers',
            'ital': 'File'
        },

        'domain': {
            'ru': 'Домены',
            'eng': 'Domains',
            'ukr': 'Домени',
            'deut': 'Domänen',
            'esp': 'Dominios',
            'fren': 'Domaines',
            'ital': 'Domini'

        },

        'ip_address': {
            'ru': 'IP-адреса',
            'eng': 'IP Addresses',
            'ukr': 'IP-адреси',
            'deut': 'IP-Adressen',
            'esp': 'Direcciones IP',
            'fren': 'Adresses IP',
            'ital': 'Indirizzi IP'

        }
    },
    'info': {
        'ru': "•  Авторы: <a href='https://t.me/+Z4wrctbz7m40MTEy'>Infosec</a> и <a href='https://t.me/+q3a-KS46N4owZGQy'>ZeroDay</a>\n"
              "•  Предложения и жалобы: @Social_Engineering_bot\n\n"
              "•  Поддержать проект (средства идут на оплату VPS и прокси):\n\n"
              " - TRC20: <code>TCxtyTGBGPNkka6x8AKNyZUz8PYF86cC1x</code>\n\n"
              " - BTC: <code>178qpKoxcBMDcdzTQBD4NjRQwQCZkgVUhq</code>",
        'eng': "• Authors: <a href='https://t.me/+Z4wrctbz7m40MTEy'>Infosec</a> and <a href='https://t.me/+q3a-KS46N4owZGQy'>ZeroDay</a>\n"
               "• Suggestions and complaints: @Social_Engineering_bot\n\n"
               "• Support the project (funds go towards VPS and proxies):\n\n"
               " - TRC20: <code>TCxtyTGBGPNkka6x8AKNyZUz8PYF86cC1x</code>\n\n"
               " - BTC: <code>178qpKoxcBMDcdzTQBD4NjRQwQCZkgVUhq</code>",

        'ukr': "• Автори: <a href='https://t.me/+Z4wrctbz7m40MTEy'>Infosec</a> і <a href='https://t.me/+q3a-KS46N4owZGQy'>ZeroDay</a>\n"
               "• Пропозиції та скарги: @Social_Engineering_bot\n\n"
               "• Підтримати проект (кошти йдуть на оплату VPS та проксі):\n\n"
               " - TRC20: <code>TCxtyTGBGPNkka6x8AKNyZUz8PYF86cC1x</code>\n\n"
               " - BTC: <code>178qpKoxcBMDcdzTQBD4NjRQwQCZkgVUhq</code>",

        'deut': "• Autoren: <a href='https://t.me/+Z4wrctbz7m40MTEy'>Infosec</a> und <a href='https://t.me/+q3a-KS46N4owZGQy'>ZeroDay</a>\n"
                "• Vorschläge und Beschwerden: @Social_Engineering_bot\n\n"
                "• Unterstützung des Projekts (Gelder werden für VPS und Proxies verwendet):\n\n"
                " - TRC20: <code>TCxtyTGBGPNkka6x8AKNyZUz8PYF86cC1x</code>\n\n"
                " - BTC: <code>178qpKoxcBMDcdzTQBD4NjRQwQCZkgVUhq</code>",

        'esp': "• Autores: <a href='https://t.me/+Z4wrctbz7m40MTEy'>Infosec</a> y <a href='https://t.me/+q3a-KS46N4owZGQy'>ZeroDay</a>\n"
               "• Sugerencias y quejas: @Social_Engineering_bot\n\n"
               "• Apoya el proyecto (los fondos se destinan a VPS y proxies):\n\n"
               " - TRC20: <code>TCxtyTGBGPNkka6x8AKNyZUz8PYF86cC1x</code>\n\n"
               " - BTC: <code>178qpKoxcBMDcdzTQBD4NjRQwQCZkgVUhq</code>",

        'fren': "• Auteurs : <a href='https://t.me/+Z4wrctbz7m40MTEy'>Infosec</a> et <a href='https://t.me/+q3a-KS46N4owZGQy'>ZeroDay</a>\n"
                "• Suggestions et réclamations : @Social_Engineering_bot\n\n"
                "• Soutenir le projet (les fonds sont utilisés pour les serveurs VPS et les proxies) :\n\n"
                " - TRC20 : <code>TCxtyTGBGPNkka6x8AKNyZUz8PYF86cC1x</code>\n\n"
                " - BTC : <code>178qpKoxcBMDcdzTQBD4NjRQwQCZkgVUhq</code>",

        'ital': "• Autori: <a href='https://t.me/+Z4wrctbz7m40MTEy'>Infosec</a> e <a href='https://t.me/+q3a-KS46N4owZGQy'>ZeroDay</a>\n"
                "• Suggerimenti e reclami: @Social_Engineering_bot\n\n"
                "• Supporta il progetto (i fondi vengono utilizzati per VPS e proxy):\n\n"
                " - TRC20: <code>TCxtyTGBGPNkka6x8AKNyZUz8PYF86cC1x</code>\n\n"
                " - BTC: <code>178qpKoxcBMDcdzTQBD4NjRQwQCZkgVUhq</code>"
    },
    'scan_menu_antivirus': {
        'ru': 'Обнаружения',
        'eng': 'Detection',
        'ukr': 'Виявлення',
        'deut': 'Erkennung',
        'esp': 'Detección',
        'fren': 'Détection',
        'ital': 'Rilevamento'

    },
    'scan_menu_signature': {
        'ru': 'Сигнатуры',
        'eng': 'Signatures',
        'ukr': 'Сигнатури',
        'deut': 'Signaturen',
        'esp': 'Firmas',
        'fren': 'Signatures',
        'ital': 'Firma'

    },
    'scan_menu_close': {
        'ru': 'Закрыть',
        'eng': 'Close',
        'ukr': 'Закрити',
        'deut': 'Schließen',
        'esp': 'Cerrar',
        'fren': 'Fermer',
        'ital': 'Chiudere'
    },
    'scan_file_texts': {
        'download_file': {
            'ru': 'Скачиваю файл',
            'eng': 'Downloading file',
            'ukr': 'Завантажую файл',
            'deut': 'Lade die Datei herunter',
            'esp': 'Descargando archivo',
            'fren': 'Téléchargement du fichier',
            'ital': 'Scaricando il file'
        },
        'download_completed': {
            'ru': '✅Файл скачен',
            'eng': '✅File downloaded',
            'ukr': '✅Файл завантажено',
            'deut': '✅Datei heruntergeladen',
            'esp': '✅Archivo descargado',
            'fren': '✅Fichier téléchargé',
            'ital': '✅File scaricato'
        },
        'load_virus_total': {
            'ru': 'Заливаю файл на VirusTotal...',
            'eng': 'Uploading file to VirusTotal...',
            'ukr': 'Завантажую файл на VirusTotal...',
            'deut': 'Lade Datei auf VirusTotal hoch...',
            'esp': 'Cargando archivo a VirusTotal...',
            'fren': 'Chargement du fichier sur VirusTotal...',
            'ital': 'Caricamento del file su VirusTotal...'
        },
        'load_virus_total_complited': {
            'ru': '✅Файл загружен на VirusTotal',
            'eng': '✅File uploaded to VirusTotal',
            'ukr': '✅Файл завантажено на VirusTotal',
            'deut': '✅Datei auf VirusTotal hochgeladen',
            'esp': '✅Archivo cargado en VirusTotal',
            'fren': '✅Fichier chargé sur VirusTotal',
            'ital': '✅File caricato su VirusTotal'
        },
        'analiz_file': {
            'ru': 'Анализ файла...',
            'eng': 'File analysis...',
            'ukr': 'Аналіз файлу...',
            'deut': 'Dateianalyse...',
            'esp': 'Análisis de archivo...',
            'fren': 'Analyse de fichier...',
            'ital': 'Analisi del file...'
        },
        'analiz_complited': {
            'ru': '✅Анализ готов',
            'eng': '✅Analysis ready',
            'ukr': '✅Аналіз готовий',
            'deut': '✅Analyse bereit',
            'esp': '✅Análisis listo',
            'fren': '✅Analyse prête',
            'ital': '✅Analisi pronta'
        },
        'file_find': {
            'ru': '✅Файл найден в базе',
            'eng': '✅File found in the database',
            'ukr': '✅Файл знайдений в базі',
            'deut': '✅Datei in der Datenbank gefunden',
            'esp': '✅Archivo encontrado en la base de datos',
            'fren': '✅Fichier trouvé dans la base de données',
            'ital': '✅File trovato nel database'
        },
        'result_text': {
            'ru': '<b>🔎 Обнаружения:</b>\n\n'
                  '❌ Обнаружения: {bad_find}\n'
                  '⚠️Подозрения: {warn_find}\n'
                  '✅Не обнаружено: {nofind}\n\n'
                  '<b>• Имя файла:</b> {file_name}\n'
                  '<b>• Формат файла:</b> {format_file}\n'
                  '<b>• Размер файла:</b> {size_file_text}\n\n'
                  '<b>• Первый анализ:</b> {first_scan}\n\n'
                  '<b>• Последний анализ:</b> {last_scan}\n\n'
                  '<b>•<a href="{link}"> Ссылка на VirusTotal</a></b>',

            'eng': '<b>🔎 Findings:</b>\n\n'
                   '❌ Detection: {bad_find}\n'
                   '⚠️ Suspicion: {warn_find}\n'
                   '✅ Not detected: {nofind}\n\n'
                   '<b>• File name:</b> {file_name}\n'
                   '<b>• File format:</b> {format_file}\n'
                   '<b>• File size:</b> {size_file_text}\n\n'
                   '<b>• First analysis:</b> {first_scan}\n\n'
                   '<b>• Last analysis:</b> {last_scan}\n\n'
                   '<b>• <a href="{link}">VirusTotal link</a></b>',
            'ukr': '<b>🔎 Виявлення:</b>\n\n'
                   '❌ Виявлення: {bad_find}\n'
                   '⚠️ Підозра: {warn_find}\n'
                   '✅ Не виявлено: {nofind}\n\n'
                   '<b>• Ім\'я файлу:</b> {file_name}\n'
                   '<b>• Формат файлу:</b> {format_file}\n'
                   '<b>• Розмір файлу:</b> {size_file_text}\n\n'
                   '<b>• Перший аналіз:</b> {first_scan}\n\n'
                   '<b>• Останній аналіз:</b> {last_scan}\n\n'
                   '<b>• <a href="{link}">Посилання на VirusTotal</a></b>',
            'deut': '<b>🔎 Ergebnisse:</b>\n\n'
                    '❌ Erkennung: {bad_find}\n'
                    '⚠️ Verdacht: {warn_find}\n'
                    '✅ Nicht erkannt: {nofind}\n\n'
                    '<b>• Dateiname:</b> {file_name}\n'
                    '<b>• Dateiformat:</b> {format_file}\n'
                    '<b>• Dateigröße:</b> {size_file_text}\n\n'
                    '<b>• Erste Analyse:</b> {first_scan}\n\n'
                    '<b>• Letzte Analyse:</b> {last_scan}\n\n'
                    '<b>• <a href="{link}">VirusTotal-Link</a></b>',
            'esp': '<b>🔎 Resultados:</b>\n\n'
                   '❌ Detección: {bad_find}\n'
                   '⚠️ Sospecha: {warn_find}\n'
                   '✅ No detectado: {nofind}\n\n'
                   '<b>• Nombre del archivo:</b> {file_name}\n'
                   '<b>• Formato del archivo:</b> {format_file}\n'
                   '<b>• Tamaño del archivo:</b> {size_file_text}\n\n'
                   '<b>• Primera análisis:</b> {first_scan}\n\n'
                   '<b>• Última análisis:</b> {last_scan}\n\n'
                   '<b>• <a href="{link}">Enlace de VirusTotal</a></b>',
            'fren': '<b>🔎 Résultats:</b>\n\n'
                    '❌ Détection: {bad_find}\n'
                    '⚠️ Suspicion: {warn_find}\n'
                    '✅ Non détecté: {nofind}\n\n'
                    '<b>• Nom du fichier:</b> {file_name}\n'
                    '<b>• Format du fichier:</b> {format_file}\n'
                    '<b>• Taille du fichier:</b> {size_file_text}\n\n'
                    '<b>• Première analyse:</b> {first_scan}\n\n'
                    '<b>• Dernière analyse:</b> {last_scan}\n\n'
                    '<b>• <a href="{link}">Lien VirusTotal</a></b>',
            'ital': '<b>🔎 Risultati:</b>\n\n'
                    '❌ Rilevamento: {bad_find}\n'
                    '⚠️ Sospetto: {warn_find}\n'
                    '✅ Non rilevato: {nofind}\n\n'
                    '<b>• Nome del file:</b> {file_name}\n'
                    '<b>• Formato del file:</b> {format_file}\n'
                    '<b>• Dimensione del file:</b> {size_file_text}\n\n'
                    '<b>• Prima analisi:</b> {first_scan}\n\n'
                    '<b>• Ultima analisi:</b> {last_scan}\n\n'
                    '<b>• <a href="{link}">Link di VirusTotal</a></b>',
        },
        'link': {
            'ru': '<b>•<a href="{link}"> Ссылка на VirusTotal</a></b>',
            'eng': '<b>•<a href="{link}"> Link to VirusTotal</a></b>',
            'ukr': '<b>•<a href="{link}"> Посилання на VirusTotal</a></b>',
            'deut': '<b>•<a href="{link}"> Link zu VirusTotal</a></b>',
            'esp': '<b>•<a href="{link}"> Enlace a VirusTotal</a></b>',
            'fren': '<b>•<a href="{link}"> Lien vers VirusTotal</a></b>',
            'ital': '<b>•<a href="{link}"> Link a VirusTotal</a></b>',
        },
        'detection': {
            'ru': '🧪Обнаружения',
            'eng': '🧪Detections',
            'ukr': '🧪Виявлення',
            'deut': '🧪Erkennungen',
            'esp': '🧪Detecciones',
            'fren': '🧪Détections',
            'ital': '🧪Rilevazioni'
        },
        'signature': {
            'ru': '💉 Сигнатуры',
            'eng': '💉 Signatures',
            'ukr': '💉 Сигнатури',
            'deut': '💉 Signaturen',
            'esp': '💉 Firmas',
            'fren': '💉 Signatures',
            'ital': '💉 Firma'
        },
        'close': {
            'ru': '❌ Закрыть',
            'eng': '❌ Close',
            'ukr': '❌ Закрити',
            'deut': '❌ Schließen',
            'esp': '❌ Cerrar',
            'fren': '❌ Fermer',
            'ital': '❌ Chiudere'
        },
        'back': {
            'ru': '🔙 Назад',
            'eng': '🔙 Back',
            'ukr': '🔙 Назад',
            'deut': '🔙 Zurück',
            'esp': '🔙 Atrás',
            'fren': '🔙 Retour',
            'ital': '🔙 Indietro'
        }},

    'big_file': {
        'ru': 'Файл слишком большой, можно сканировать файлы до 650мб',
        'eng': 'The file is too large, files up to 650MB can be scanned',
        'ukr': 'Файл занадто великий, можна сканувати файли розміром до 650МБ',
        'deut': 'Die Datei ist zu groß, Dateien bis zu 650 MB können gescannt werden',
        'esp': 'El archivo es demasiado grande, se pueden escanear archivos de hasta 650MB',
        'fren': 'Le fichier est trop volumineux, il est possible de scanner des fichiers jusqu\'à 650 Mo',
        'ital': 'Il file è troppo grande, è possibile scansionare file fino a 650MB'
    },
    'no_signature': {
        'ru': 'Обнаружений нету',
        'eng': 'No detections found',
        'ukr': 'Виявлень немає',
        'deut': 'Keine Erkennungen gefunden',
        'esp': 'No se encontraron detecciones',
        'fren': 'Aucune détection trouvée',
        'ital': 'Nessuna rilevazione trovata',
    },
    'flood': {
        'ru': '<b>Можно обрабатывать 1 файл раз в 4 минуты</b>',
        'eng': '<b>1 file can be processed once every 4 minutes</b>',
        'ukr': '<b>Можна обробляти 1 файл один раз у 4 хвилини</b>',
        'deut': '<b>1 Datei kann alle 4 Minuten einmal verarbeitet werden</b>',
        'esp': '<b>Se puede procesar 1 archivo una vez cada 4 minutos</b>',
        'fren': '<b>1 fichier peut être traité une fois toutes les 4 minutes</b>',
        'ital': '<b>1 file può essere elaborato una volta ogni 4 minuti</b>'
    },
    'ip_address_info': {
        'ru': '<b>🔎 Обнаружения:</b>\n\n'
              '❌ Обнаружения: {bad_find}\n'
              '⚠️Подозрения: {warn_find}\n'
              '✅Не обнаружено: {nofind}\n\n'
              '• Адрес: {ip_address}\n'
              '• Сеть: {network}\n'
              '• Страна: {country}\n'
              '• Последнее сканирование: {last_scan}\n\n'
              '• <b><a href="https://www.virustotal.com/gui/ip-address/{ip_address}">Ссылка на VirusTotal</a></b>',
        'eng': '<b>🔎 Findings:</b>\n\n'
               '❌ Findings: {bad_find}\n'
               '⚠️ Suspicious: {warn_find}\n'
               '✅ Not detected: {nofind}\n\n'
               '• Address: {ip_address}\n'
               '• Network: {network}\n'
               '• Country: {country}\n'
               '• Last scan: {last_scan}\n\n'
               '• <b><a href="https://www.virustotal.com/gui/ip-address/{ip_address}">Link to VirusTotal</a></b>',

        'ukr': '<b>🔎 Виявлення:</b>\n\n'
               '❌ Виявлення: {bad_find}\n'
               '⚠️ Підозрілість: {warn_find}\n'
               '✅ Не виявлено: {nofind}\n\n'
               '• Адреса: {ip_address}\n'
               '• Мережа: {network}\n'
               '• Країна: {country}\n'
               '• Останнє сканування: {last_scan}\n\n'
               '• <b><a href="https://www.virustotal.com/gui/ip-address/{ip_address}">Посилання на VirusTotal</a></b>',

        'deut': '<b>🔎 Ergebnisse:</b>\n\n'
                '❌ Ergebnisse: {bad_find}\n'
                '⚠️ Verdächtigungen: {warn_find}\n'
                '✅ Nicht erkannt: {nofind}\n\n'
                '• Adresse: {ip_address}\n'
                '• Netzwerk: {network}\n'
                '• Land: {country}\n'
                '• Letzter Scan: {last_scan}\n\n'
                '• <b><a href="https://www.virustotal.com/gui/ip-address/{ip_address}">Link zu VirusTotal</a></b>',

        'esp': '<b>🔎 Resultados:</b>\n\n'
               '❌ Resultados: {bad_find}\n'
               '⚠️ Sospechas: {warn_find}\n'
               '✅ No detectado: {nofind}\n\n'
               '• Dirección: {ip_address}\n'
               '• Red: {network}\n'
               '• País: {country}\n'
               '• Último escaneo: {last_scan}\n\n'
               '• <b><a href="https://www.virustotal.com/gui/ip-address/{ip_address}">Enlace a VirusTotal</a></b>',

        'fren': '<b>🔎 Résultats:</b>\n\n'
                '❌ Résultats: {bad_find}\n'
                '⚠️ Suspicions: {warn_find}\n'
                '✅ Non détecté: {nofind}\n\n'
                '• Adresse: {ip_address}\n'
                '• Réseau: {network}\n'
                '• Pays: {country}\n'
                '• Dernière analyse: {last_scan}\n\n'
                '• <b><a href="https://www.virustotal.com/gui/ip-address/{ip_address}">Lien vers VirusTotal</a></b>',

        'ital': '<b>🔎 Risultati:</b>\n\n'
                '❌ Risultati: {bad_find}\n'
                '⚠️ Sospetti: {warn_find}\n'
                '✅ Non rilevato: {nofind}\n\n'
                '• Indirizzo: {ip_address}\n'
                '• Rete: {network}\n'
                '• Paese: {country}\n'
                '• Ultima scansione: {last_scan}\n\n'
                '• <b><a href="https://www.virustotal.com/gui/ip-address/{ip_address}">Link a VirusTotal</a></b>'

    },

    'whois_btn': {
        'ru': 'WhoIs',
        'eng': 'WhoIs',
        'ukr': 'WhoIs',
        'deut': 'WhoIs',
        'esp': 'WhoIs',
        'fren': 'WhoIs',
        'ital': 'WhoIs'},
    'whois': {
        'ru': '<b>Данные с WhoIs</b>\n\n'
              '{whois}',
        'eng': '<b>Whois data</b>\n\n'
               '{whois}',
        'ukr': '<b>Дані з WhoIs</b>\n\n'
               '{whois}',
        'deut': '<b>Whois-Daten</b>\n\n'
                '{whois}',
        'esp': '<b>Datos de Whois</b>\n\n'
               '{whois}',
        'fren': '<b>Données Whois</b>\n\n'
                '{whois}',
        'ital': '<b>Dati Whois</b>\n\n'
                '{whois}'

    },

    'domain': {
        'ru': '<b>🔎 Обнаружения:</b>\n\n'
              '❌ Обнаружения: {bad_find}\n'
              '⚠️Подозрения: {warn_find}\n'
              '✅Не обнаружено: {nofind}\n\n'
              '• Домен: {domain}\n'
              '• Последнее сканирование: {last_scan}\n'
              '• Дата создания: {creation_date}\n\n'
              '• <b><a href="https://www.virustotal.com/gui/domain/{domain}">Ссылка на VirusTotal</a></b>',
        'ukr': '<b>🔎 Виявлення:</b>\n\n'
               '❌ Виявлення: {bad_find}\n'
               '⚠️ Підозри: {warn_find}\n'
               '✅ Не виявлено: {nofind}\n\n'
               '• Домен: {domain}\n'
               '• Останнє сканування: {last_scan}\n'
               '• Дата створення: {creation_date}\n\n'
               '• <b><a href="https://www.virustotal.com/gui/domain/{domain}">Посилання на VirusTotal</a></b>',

        'eng': '<b>🔎 Findings:</b>\n\n'
               '❌ Findings: {bad_find}\n'
               '⚠️ Suspicion: {warn_find}\n'
               '✅ Not found: {nofind}\n\n'
               '• Domain: {domain}\n'
               '• Last scan: {last_scan}\n'
               '• Creation date: {creation_date}\n\n'
               '• <b><a href="https://www.virustotal.com/gui/domain/{domain}">Link to VirusTotal</a></b>',
        'deut': '<b>🔎 Erkennungen:</b>\n\n'
                '❌ Erkennungen: {bad_find}\n'
                '⚠️ Verdachte: {warn_find}\n'
                '✅ Nicht erkannt: {nofind}\n\n'
                '• Domain: {domain}\n'
                '• Letzter Scan: {last_scan}\n'
                '• Erstellungsdatum: {creation_date}\n\n'
                '• <b><a href="https://www.virustotal.com/gui/domain/{domain}">Link zu VirusTotal</a></b>',
        'esp': '<b>🔎 Detecciones:</b>\n\n'
               '❌ Detecciones: {bad_find}\n'
               '⚠️ Sospechas: {warn_find}\n'
               '✅ No detectado: {nofind}\n\n'
               '• Dominio: {domain}\n'
               '• Última exploración: {last_scan}\n'
               '• Fecha de creación: {creation_date}\n\n'
               '• <b><a href="https://www.virustotal.com/gui/domain/{domain}">Enlace a VirusTotal</a></b>',
        'fren': '<b>🔎 Détecteurs:</b>\n\n'
                '❌ Détecteurs: {bad_find}\n'
                '⚠️ Suspicion: {warn_find}\n'
                '✅ Non détecté: {nofind}\n\n'
                '• Domaine: {domain}\n'
                '• Dernière analyse: {last_scan}\n'
                '• Date de création: {creation_date}\n\n'
                '• <b><a href="https://www.virustotal.com/gui/domain/{domain}">Lien vers VirusTotal</a></b>',
        'ital': '<b>🔎 Rilevamenti:</b>\n\n'
                '❌ Rilevamenti: {bad_find}\n'
                '⚠️ Sospetti: {warn_find}\n'
                '✅ Non rilevato: {nofind}\n\n'
                '• Dominio: {domain}\n'
                '• Ultima scansione: {last_scan}\n'
                '• Data di creazione: {creation_date}\n\n'
                '• <b><a href="https://www.virustotal.com/gui/domain/{domain}">Collegamento a VirusTotal</a></b>'
    },

    'find_file': {
        'ru': 'В сообщении обнаружен файл!',
        'eng': 'A file was found in the message!',
        'ukr': 'У повідомленні виявлено файл!',
        'deut': 'In der Nachricht wurde eine Datei gefunden!',
        'esp': '¡Se encontró un archivo en el mensaje!',
        'fren': 'Un fichier a été trouvé dans le message !',
        'ital': 'Un file è stato trovato nel messaggio!'
    },
    'find_file_btn': {
        'ru': 'Сканировать',
        'eng': 'Scanning',
        'ukr': 'Сканування',
        'deut': 'Scannen',
        'esp': 'Escaneo',
        'fren': 'Analyse',
        'ital': 'Scansione'
    }

}

COUNTRY_CODE = {
    "AF": "Afghanistan 🇦🇫",
    "AL": "Albania 🇦🇱",
    "DZ": "Algeria 🇩🇿",
    "AD": "Andorra 🇦🇩",
    "AO": "Angola 🇦🇴",
    "AR": "Argentina 🇦🇷",
    "AM": "Armenia 🇦🇲",
    "AU": "Australia 🇦🇺",
    "AT": "Austria 🇦🇹",
    "AZ": "Azerbaijan 🇦🇿",
    "BS": "Bahamas 🇧🇸",
    "BH": "Bahrain 🇧🇭",
    "BD": "Bangladesh 🇧🇩",
    "BB": "Barbados 🇧🇧",
    "BY": "Belarus 🇧🇾",
    "BE": "Belgium 🇧🇪",
    "BZ": "Belize 🇧🇿",
    "BJ": "Benin 🇧🇯",
    "BT": "Bhutan 🇧🇹",
    "BO": "Bolivia 🇧🇴",
    "BA": "Bosnia and Herzegovina 🇧🇦",
    "BW": "Botswana 🇧🇼",
    "BR": "Brazil 🇧🇷",
    "BN": "Brunei 🇧🇳",
    "BG": "Bulgaria 🇧🇬",
    "BF": "Burkina Faso 🇧🇫",
    "BI": "Burundi 🇧🇮",
    "KH": "Cambodia 🇰🇭",
    "CM": "Cameroon 🇨🇲",
    "CA": "Canada 🇨🇦",
    "CF": "Central African Republic 🇨🇫",
    "TD": "Chad 🇹🇩",
    "CL": "Chile 🇨🇱",
    "CN": "China 🇨🇳",
    "CO": "Colombia 🇨🇴",
    "KM": "Comoros 🇰🇲",
    "CG": "Congo 🇨🇬",
    "CD": "Democratic Republic of the Congo 🇨🇩",
    "CR": "Costa Rica 🇨🇷",
    "HR": "Croatia 🇭🇷",
    "CU": "Cuba 🇨🇺",
    "CY": "Cyprus 🇨🇾",
    "CZ": "Czech Republic 🇨🇿",
    "DK": "Denmark 🇩🇰",
    "DJ": "Djibouti 🇩🇯",
    "DO": "Dominican Republic 🇩🇴",
    "EC": "Ecuador 🇪🇨",
    "EG": "Egypt 🇪🇬",
    "SV": "El Salvador 🇸🇻",
    "GQ": "Equatorial Guinea 🇬🇶",
    "ER": "Eritrea 🇪🇷",
    "EE": "Estonia 🇪🇪",
    "ET": "Ethiopia 🇪🇹",
    "FJ": "Fiji 🇫🇯",
    "FI": "Finland 🇫🇮",
    "FR": "France 🇫🇷",
    "GA": "Gabon 🇬🇦",
    "GM": "Gambia 🇬🇲",
    "GE": "Georgia 🇬🇪",
    "DE": "Germany 🇩🇪",
    "GH": "Ghana 🇬🇭",
    "GR": "Greece 🇬🇷",
    "GT": "Guatemala 🇬🇹",
    "GN": "Guinea 🇬🇳",
    "GW": "Guinea-Bissau 🇬🇼",
    "GY": "Guyana 🇬🇾",
    "HT": "Haiti 🇭🇹",
    "HN": "Honduras 🇭🇳",
    "HU": "Hungary 🇭🇺",
    "IS": "Iceland 🇮🇸",
    "IN": "India 🇮🇳",
    "ID": "Indonesia 🇮🇩",
    "IR": "Iran 🇮🇷",
    "IQ": "Iraq 🇮🇶",
    "IE": "Ireland 🇮🇪",
    "IL": "Israel 🇮🇱",
    "IT": "Italy 🇮🇹",
    "JM": "Jamaica 🇯🇲",
    "JP": "Japan 🇯🇵",
    "JO": "Jordan 🇯🇴",
    "KZ": "Kazakhstan 🇰🇿",
    "KE": "Kenya 🇰🇪",
    "KP": "North Korea 🇰🇵",
    "KR": "South Korea 🇰🇷",
    "KW": "Kuwait 🇰🇼",
    "KG": "Kyrgyzstan 🇰🇬",
    "LA": "Laos 🇱🇦",
    "LV": "Latvia 🇱🇻",
    "LB": "Lebanon 🇱🇧",
    "LS": "Lesotho 🇱🇸",
    "LR": "Liberia 🇱🇷",
    "LY": "Libya 🇱🇾",
    "LI": "Liechtenstein 🇱🇮",
    "LT": "Lithuania 🇱🇹",
    "LU": "Luxembourg 🇱🇺",
    "MK": "North Macedonia 🇲🇰",
    "MG": "Madagascar 🇲🇬",
    "MW": "Malawi 🇲🇼",
    "MY": "Malaysia 🇲🇾",
    "MV": "Maldives 🇲🇻",
    "ML": "Mali 🇲🇱",
    "MT": "Malta 🇲🇹",
    "MR": "Mauritania 🇲🇷",
    "MU": "Mauritius 🇲🇺",
    "MX": "Mexico 🇲🇽",
    "FM": "Micronesia 🇫🇲",
    "MD": "Moldova 🇲🇩",
    "MC": "Monaco 🇲🇨",
    "MN": "Mongolia 🇲🇳",
    "ME": "Montenegro 🇲🇪",
    "MA": "Morocco 🇲🇦",
    "MZ": "Mozambique 🇲🇿",
    "MM": "Myanmar 🇲🇲",
    "NA": "Namibia 🇳🇦",
    "NR": "Nauru 🇳🇷",
    "NP": "Nepal 🇳🇵",
    "NL": "Netherlands 🇳🇱",
    "NZ": "New Zealand 🇳🇿",
    "NI": "Nicaragua 🇳🇮",
    "NE": "Niger 🇳🇪",
    "NG": "Nigeria 🇳🇬",
    "NO": "Norway 🇳🇴",
    "OM": "Oman 🇴🇲",
    "PK": "Pakistan 🇵🇰",
    "PW": "Palau 🇵🇼",
    "PA": "Panama 🇵🇦",
    "PG": "Papua New Guinea 🇵🇬",
    "PY": "Paraguay 🇵🇾",
    "PE": "Peru 🇵🇪",
    "PH": "Philippines 🇵🇭",
    "PL": "Poland 🇵🇱",
    "PT": "Portugal 🇵🇹",
    "QA": "Qatar 🇶🇦",
    "RO": "Romania 🇷🇴",
    "RU": "Russia 🇷🇺",
    "RW": "Rwanda 🇷🇼",
    "KN": "Saint Kitts and Nevis 🇰🇳",
    "LC": "Saint Lucia 🇱🇨",
    "VC": "Saint Vincent and the Grenadines 🇻🇨",
    "WS": "Samoa 🇼🇸",
    "SM": "San Marino 🇸🇲",
    "ST": "Sao Tome and Principe 🇸🇹",
    "SA": "Saudi Arabia 🇸🇦",
    "SN": "Senegal 🇸🇳",
    "RS": "Serbia 🇷🇸",
    "SC": "Seychelles 🇸🇨",
    "SL": "Sierra Leone 🇸🇱",
    "SG": "Singapore 🇸🇬",
    "SK": "Slovakia 🇸🇰",
    "SI": "Slovenia 🇸🇮",
    "SB": "Solomon Islands 🇸🇧",
    "SO": "Somalia 🇸🇴",
    "ZA": "South Africa 🇿🇦",
    "SS": "South Sudan 🇸🇸",
    "ES": "Spain 🇪🇸",
    "LK": "Sri Lanka 🇱🇰",
    "SD": "Sudan 🇸🇩",
    "SR": "Suriname 🇸🇷",
    "SE": "Sweden 🇸🇪",
    "CH": "Switzerland 🇨🇭",
    "SY": "Syria 🇸🇾",
    "TJ": "Tajikistan 🇹🇯",
    "TZ": "Tanzania 🇹🇿",
    "TH": "Thailand 🇹🇭",
    "TL": "Timor-Leste 🇹🇱",
    "TG": "Togo 🇹🇬",
    "TO": "Tonga 🇹🇴",
    "TT": "Trinidad and Tobago 🇹🇹",
    "TN": "Tunisia 🇹🇳",
    "TR": "Turkey 🇹🇷",
    "TM": "Turkmenistan 🇹🇲",
    "TV": "Tuvalu 🇹🇻",
    "UG": "Uganda 🇺🇬",
    "UA": "Ukraine 🇺🇦",
    "AE": "United Arab Emirates 🇦🇪",
    "GB": "United Kingdom 🇬🇧",
    "US": "United States 🇺🇸",
    "UY": "Uruguay 🇺🇾",
    "UZ": "Uzbekistan 🇺🇿",
    "VU": "Vanuatu 🇻🇺",
    "VA": "Vatican City 🇻🇦",
    "VE": "Venezuela 🇻🇪",
    "VN": "Vietnam 🇻🇳",
    "YE": "Yemen 🇾🇪",
    "ZM": "Zambia 🇿🇲",
    "ZW": "Zimbabwe 🇿🇼"
}
