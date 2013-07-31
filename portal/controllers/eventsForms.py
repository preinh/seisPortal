
import tw2.core as twc
import tw2.forms as twf
import tw2.dynforms as twd
import tw2.jqplugins.ui as jqui



class EventFilterForm(twf.Form):
    submit = None
    action = None
    class child(twf.RowLayout):
        repetition = 1
    
        class timeWindow(twf.TableLayout):
            
            id = None
            #repetitions = 1
            date_f = jqui.widgets.DateTimePickerWidget(id="date_f",
                                                       label="De", 
                                                       size=12,
                                              options={
                                                       'dateFormat':'dd-mm-yy',
                                                       },
                                              events={
                                                  'onClose': """ 
                                                        function(dateText, inst) {
                                                            if ($('#date_t').val() != '') {
                                                                var testStartDate = $('#date_f').datetimepicker('getDate');
                                                                var portalndDate = $('#date_t').datetimepicker('getDate');
                                                                if (testStartDate > portalndDate)
                                                                    $('#date_t').datetimepicker('setDate', testStartDate);
                                                            }
                                                            else {
                                                                $('#date_t').val(dateText);
                                                            }
                                                        }"""
                                                        ,
                                                    'onSelect': """
                                                        function (selectedDateTime){
                                                            $('#date_t').datetimepicker('option', 
                                                                                          'minDate', 
                                                                                          $('#date_f').datetimepicker('getDate') 
                                                                                          );
                                                        }"""
                                                        ,
                                                    }
                                              )
            
            date_t = jqui.widgets.DateTimePickerWidget(id="date_t",
                                                       label="Ate", 
                                                       size=12,
                                              options={
                                                       'dateFormat':'dd-mm-yy',
                                                       },
                                              events={
                                                  'onClose': """ 
                                                        function(dateText, inst) {
                                                             if ($('#date_f').val() != '') {
                                                                var testStartDate = $('#date_f').datetimepicker('getDate');
                                                                var portalndDate = $('#date_t').datetimepicker('getDate');
                                                                if (testStartDate > portalndDate)
                                                                    $('#date_f').datetimepicker('setDate', portalndDate);
                                                            }
                                                            else {
                                                                $('#date_f').val(dateText);
                                                            }
                                                    }"""
                                                        ,
                                                    'onSelect': """
                                                        function (selectedDateTime){
                                                            $('#date_f').datetimepicker('option', 
                                                                                            'maxDate', 
                                                                                            $('#date_t').datetimepicker('getDate') 
                                                                                            );
                                                        }
                                                        """
                                                    }
                                              )

        class lat(twf.ListLayout):
            id=None
            lat_f = twf.HiddenField()
            lat_t = twf.HiddenField()
            lat = jqui.widgets.SliderWidget("Latitude",
                                            options={
                                            'range': True,
                                            'min' : -90,
                                            'max' : 90,
                                            'step' : 0.01,
                                            'values' : [-35, 6],
                                                     },
                                            events={
                                                    'slide' : """  
                                                            function( event, ui ) {
                                                                $( "#lat_f"  ).val(ui.values[ 0 ]);
                                                                $( "#lat_t" ).val(ui.values[ 1 ]);
                                                                $( "#lblLat" ).val(ui.values[ 0 ]+" a "+ui.values[ 1 ]);
                                                            }
                                                            """,
                                                    })
            lblLat = twf.TextField(label=None, size=10, attrs={'style': "border: 0;", 'readonly':'readonly'})
        
        class lon(twf.ListLayout):
            id = None
            lon_f = twf.HiddenField()
            lon_t = twf.HiddenField()
            lon = jqui.widgets.SliderWidget(id="Longitude",
                                            options={
                                            'range': True,
                                            'min' : -180,
                                            'max' : 180,
                                            'step' : 0.01,
                                            'values' : [-90, -35],
                                                     },
                                            events={
                                                    'slide' : """  
                                                            function( event, ui ) {
                                                                $( "#lon_f"  ).val(ui.values[ 0 ]);
                                                                $( "#lon_t" ).val(ui.values[ 1 ]);
                                                                $( "#lblLon" ).val(ui.values[ 0 ]+" a "+ui.values[ 1 ]);
                                                            }
                                                            """,
                                                    })
            lblLon = twf.TextField(label=None,  size=10, attrs={'style': "border: 0;", 'readonly':'readonly'})

        class dep(twf.ListLayout):
            id=None
            dep_f = twf.HiddenField()
            dep_t = twf.HiddenField()
            dep = jqui.widgets.SliderWidget("profundidade",
                                            options={
                                            'range': True,
                                            'min' : 0,
                                            'max' : 6500,
                                            'step' : 1.0,
                                            'values' : [0, 800],
                                                     },
                                            events={
                                                    'slide' : """  
                                                            function( event, ui ) {
                                                                $( "#dep_f"  ).val(ui.values[ 0 ]);
                                                                $( "#dep_t" ).val(ui.values[ 1 ]);
                                                                $( "#lblDep" ).val(ui.values[ 0 ]+" a "+ui.values[ 1 ]);
                                                            }
                                                            """,
                                                    })
            lblDep = twf.TextField(label=None, size=10, attrs={'style': "border: 0;", 'readonly':'readonly'})
        
        class mag(twf.ListLayout):
            id=None
            mag_f = twf.HiddenField()
            mag_t = twf.HiddenField()
            mag = jqui.widgets.SliderWidget("magnitude",
                                            options={
                                            'range': True,
                                            'min' : -5,
                                            'max' : 12,
                                            'step' : 0.01,
                                            'values' : [0, 10],
                                                     },
                                            events={
                                                    'slide' : """  
                                                            function( event, ui ) {
                                                                $( "#mag_f"  ).val(ui.values[ 0 ]);
                                                                $( "#mag_t" ).val(ui.values[ 1 ]);
                                                                $( "#lblMag" ).val(ui.values[ 0 ]+" a "+ui.values[ 1 ]);
                                                            }
                                                            """,
                                                    })
            lblMag = twf.TextField(label=None, size=10, attrs={'style': "border: 0;", 'readonly':'readonly'})

        class do(twf.SubmitButton):
            value="Filtrar"
