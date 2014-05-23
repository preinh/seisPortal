
import tw2.core as twc
import tw2.forms as twf
import tw2.dynforms as twd
import tw2.jqplugins.ui as jqui



class BsbFilterForm(twf.Form):
    submit = None
    action = None


    class child(twf.RowLayout):
        repetition = 1
    
        class bsb_timeWindow(twf.TableLayout):
            
            id = None
            #repetitions = 1
            bsb_date_f = jqui.widgets.DateTimePickerWidget(id="bsb_date_f",
                                                       label="De", 
                                                       size=12,
                                              options={
                                                       'dateFormat':'dd-mm-yy',
                                                       },
                                              events={
                                                  'onClose': """ 
                                                        function(dateText, inst) {
                                                            if ($('#bsb_date_t').val() != '') {
                                                                var bsb_testStartDate = $('#bsb_date_f').datetimepicker('getDate');
                                                                var bsb_portalndDate = $('#bsb_date_t').datetimepicker('getDate');
                                                                if (bsb_testStartDate > bsb_portalndDate)
                                                                    $('#bsb_date_t').datetimepicker('setDate', bsb_testStartDate);
                                                            }
                                                            else {
                                                                $('#bsb_date_t').val(dateText);
                                                            }
                                                        }"""
                                                        ,
                                                    'onSelect': """
                                                        function (selectedDateTime){
                                                            $('#bsb_date_t').datetimepicker('option',
                                                                                          'minDate', 
                                                                                          $('#bsb_date_f').datetimepicker('getDate')
                                                                                          );
                                                        }"""
                                                        ,
                                                    }
                                              )

            bsb_date_t = jqui.widgets.DateTimePickerWidget(id="bsb_date_t",
                                                       label="Ate", 
                                                       size=12,
                                              options={
                                                       'dateFormat':'dd-mm-yy',
                                                       },
                                              events={
                                                  'onClose': """ 
                                                        function(dateText, inst) {
                                                             if ($('#bsb_date_f').val() != '') {
                                                                var bsb_testStartDate = $('#bsb_date_f').datetimepicker('getDate');
                                                                var bsb_portalndDate  = $('#bsb_date_t').datetimepicker('getDate');
                                                                if (bsb_testStartDate > bsb_portalndDate)
                                                                    $('#bsb_date_f').datetimepicker('setDate', bsb_portalndDate);
                                                            }
                                                            else {
                                                                $('#bsb_date_f').val(dateText);
                                                            }
                                                    }"""
                                                        ,
                                                    'onSelect': """
                                                        function (selectedDateTime){
                                                            $('#bsb_date_f').datetimepicker('option',
                                                                                            'maxDate', 
                                                                                            $('#bsb_date_t').datetimepicker('getDate')
                                                                                            );
                                                        }
                                                        """
                                                    }
                                              )

        class bsb_lat(twf.ListLayout):
            id=None
            bsb_lat_f = twf.HiddenField()
            bsb_lat_t = twf.HiddenField()
            bsb_lat = jqui.widgets.SliderWidget(
                                            id="bsb_latitude",
                                            label="Latitude",
                                            options={
                                            'range': True,
                                            'min' : -90,
                                            'max' : 90,
                                            'step' : 10.0,
                                            'values' : [-35, 6],
                                                     },
                                            events={
                                                    'slide' : """  
                                                            function( event, ui ) {
                                                                $( "#bsb_lat_f"  ).val(ui.values[ 0 ]);
                                                                $( "#bsb_lat_t" ).val(ui.values[ 1 ]);
                                                                $( "#bsb_lblLat" ).val(ui.values[ 0 ]+" a "+ui.values[ 1 ]);
                                                            }
                                                            """,
                                                    })
            bsb_lblLat = twf.TextField(label=None, size=15, attrs={'style': "border: 0;", 'readonly':'readonly'})
        
        class bsb_lon(twf.ListLayout):
            id = None
            bsb_lon_f = twf.HiddenField()
            bsb_lon_t = twf.HiddenField()
            bsb_lon = jqui.widgets.SliderWidget(
                                            id="bsb_longitude",
                                            label="Longitude",
                                            options={
                                            'range': True,
                                            'min' : -180,
                                            'max' : 180,
                                            'step' : 10.0,
                                            'values' : [-90, -35],
                                                     },
                                            events={
                                                    'slide' : """  
                                                            function( event, ui ) {
                                                                $( "#bsb_lon_f"  ).val(ui.values[ 0 ]);
                                                                $( "#bsb_lon_t" ).val(ui.values[ 1 ]);
                                                                $( "#bsb_lblLon" ).val(ui.values[ 0 ]+" a "+ui.values[ 1 ]);
                                                            }
                                                            """,
                                                    })
            bsb_lblLon = twf.TextField(label=None,  size=15, attrs={'style': "border: 0;", 'readonly':'readonly'})

        class bsb_dep(twf.ListLayout):
            id=None
            bsb_dep_f = twf.HiddenField()
            bsb_dep_t = twf.HiddenField()
            bsb_dep = jqui.widgets.SliderWidget(
                                            id="bsb_dep",
                                            label="profundidade",
                                            options={
                                            'range': True,
                                            'min' : 0,
                                            'max' : 800,
                                            'step' : 5.0,
                                            'values' : [0, 800],
                                                     },
                                            events={
                                                    'slide' : """  
                                                            function( event, ui ) {
                                                                $( "#bsb_dep_f"  ).val(ui.values[ 0 ]);
                                                                $( "#bsb_dep_t" ).val(ui.values[ 1 ]);
                                                                $( "#bsb_lblDep" ).val(ui.values[ 0 ]+" a "+ui.values[ 1 ]);
                                                            }
                                                            """,
                                                    })
            bsb_lblDep = twf.TextField(label=None, size=15, attrs={'style': "border: 0;", 'readonly':'readonly'})
        
        class bsb_mag(twf.ListLayout):
            id=None
            bsb_mag_f = twf.HiddenField()
            bsb_mag_t = twf.HiddenField()
            bsb_mag = jqui.widgets.SliderWidget(
                                            id="bsb_mag",
                                            label="magnitude",
                                            options={
                                            'range': True,
                                            'min' : -5,
                                            'max' : 10,
                                            'step' : 0.5,
                                            'values' : [0, 10],
                                                     },
                                            events={
                                                    'slide' : """  
                                                            function( event, ui ) {
                                                                $( "#bsb_mag_f"  ).val(ui.values[ 0 ]);
                                                                $( "#bsb_mag_t" ).val(ui.values[ 1 ]);
                                                                $( "#bsb_lblMag" ).val(ui.values[ 0 ]+" a "+ui.values[ 1 ]);
                                                            }
                                                            """,
                                                    })
            bsb_lblMag = twf.TextField(label=None, size=15, attrs={'style': "border: 0;", 'readonly':'readonly'})

        class bsb_do(twf.SubmitButton):
            value="Filtrar"
