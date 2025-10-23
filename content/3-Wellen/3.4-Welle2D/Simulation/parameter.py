start_var = 0
gridfct = None
geodomain = None

scale_sender = 1
scale_prism = 1
scale_lens = 1

scale_domain = 1
mat_thickness = 0.0025
current_rpml = 0.4
radius_outer = 0.56




resolution="""require(
        ["base/js/dialog"], 
        function(dialog) {
            dialog.modal({
                title: 'Warnung',
                body: 'Die Auflösung ist schlecht. Vor der Auswertung bitte Polynomgrad erhöhen oder Gitterbreite oder Wellenzahl verringern.',
                buttons: {
                    'Schließen':{},
                }
            });
        }
    );"""

error_name="""require(
        ["base/js/dialog"], 
        function(dialog) {
            dialog.modal({
                title: 'Fehler',
                body: 'Name bereits vorhanden. Bitte anderen Namen wählen',
                buttons: {
                    'Schließen':{},
                }
            });
        }
    );"""

warning_outside="""require(
        ["base/js/dialog"], 
        function(dialog) {
            dialog.modal({
                title: 'Warnung',
                body: 'Das Objekt befindet sich möglicherweise außerhalb des zulässigen Gebiets.',
                buttons: {
                    'Schließen':{},
                }
            });
        }
    );"""

warning_outside2="""require(
        ["base/js/dialog"], 
        function(dialog) {
            dialog.modal({
                title: 'Warnung',
                body: 'Teile des Kreisbogens befinden sich außerhalb des Gebietes.',
                buttons: {
                    'Schließen':{},
                }
            });
        }
    );"""

warning_overlap="""require(
        ["base/js/dialog"], 
        function(dialog) {
            dialog.modal({
                title: 'Warnung',
                body: 'Das Objekt schneidet möglicherweise ein anderes Objekt.',
                buttons: {
                    'Schließen':{},
                }
            });
        }
    );"""

error_sender="""require(
        ["base/js/dialog"], 
        function(dialog) {
            dialog.modal({
                title: 'Fehler',
                body: 'Es wurde bereits ein Sender hinzugefügt.',
                buttons: {
                    'Schließen':{},
                }
            });
        }
    );"""

error_sender2="""require(
        ["base/js/dialog"], 
        function(dialog) {
            dialog.modal({
                title: 'Fehler',
                body: 'Es wurde noch kein Sender hinzugefügt.',
                buttons: {
                    'Schließen':{},
                }
            });
        }
    );"""


error_missing="""require(
        ["base/js/dialog"], 
        function(dialog) {
            dialog.modal({
                title: 'Fehler',
                body: 'Es wurden noch nicht alle notwendigen Parameter ausgewählt',
                buttons: {
                    'Schließen':{},
                }
            });
        }
    );"""

changed="""require(
        ["base/js/dialog"], 
        function(dialog) {
            dialog.modal({
                title: 'Hinweis',
                body: 'Objekt erfolgreich geändert.',
                buttons: {
                    'Schließen':{},
                }
            });
        }
    );"""




