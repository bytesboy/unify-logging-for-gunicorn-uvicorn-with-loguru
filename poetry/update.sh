#===============================
# Poetry Update
#===============================

echo '
__________              __                   ____ ___            .___       __
\______   \____   _____/  |________ ___.__. |    |   \______   __| _/____ _/  |_  ____
 |     ___/  _ \_/ __ \   __\_  __ <   |  | |    |   /\____ \ / __ |\__  \\   __\/ __ \
 |    |  (  <_> )  ___/|  |  |  | \/\___  | |    |  / |  |_> > /_/ | / __ \|  | \  ___/
 |____|   \____/ \___  >__|  |__|   / ____| |______/  |   __/\____ |(____  /__|  \___  >
                     \/             \/                |__|        \/     \/          \/
'

ROOT="$(dirname "$(pwd)")"

cd "$ROOT" && poetry update