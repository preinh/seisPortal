
import tw2.core as twc
import tw2.forms as twf
import tw2.dynforms as twd
import tw2.jqplugins.ui as jqui


class DownloadForm(twf.Form):
    submit = None
    action = None
    class child(twf.RowLayout):
        repetition = 1


        class network(twf.ListLayout):
            id=None
            network = twf.TextField(size=2)


        class station(twf.ListLayout):
            id=None
            station = twf.TextField(size=5)

        class channel(twf.ListLayout):
            id=None
            channel = twf.TextField(size=3)


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



        class onehour(twf.ListLayout):
            id=None
            onhour = twf.CheckBox()


        class type(twf.ListLayout):
            id=None
            type=twf.SingleSelectField(options=['SAC','MSEED'])
            type.value = 'SAC'

        class do(twf.SubmitButton):
            value="Download"
