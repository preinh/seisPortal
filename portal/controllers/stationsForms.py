
import tw2.core as twc
import tw2.forms as twf
import tw2.dynforms as twd
import tw2.jqplugins.ui as jqui



class StationFilterForm(twf.Form):
    submit = None
    action = None
    class child(twf.RowLayout):
        repetition = 1


        class cod(twf.ListLayout):
            id=None
            cod = twf.TextField(size=6)


        class loc(twf.ListLayout):
            id=None
            loc = twf.TextField(size=25)



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
            lblLat = twf.TextField(label=None, size=8, attrs={'style': "border: 0;", 'readonly':'readonly'})
        
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
            lblLon = twf.TextField(label=None,  size=8, attrs={'style': "border: 0;", 'readonly':'readonly'})

        class dep(twf.ListLayout):
            id=None
            dep_f = twf.HiddenField()
            dep_t = twf.HiddenField()
            dep = jqui.widgets.SliderWidget("Elevacao",
                                            options={
                                            'range': True,
                                            'min' : 0,
                                            'max' : 6000,
                                            'step' : 1.0,
                                            'values' : [0, 4000],
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
            lblDep = twf.TextField(label=None, size=8, attrs={'style': "border: 0;", 'readonly':'readonly'})
        

        class do(twf.SubmitButton):
            value="Filtrar"
