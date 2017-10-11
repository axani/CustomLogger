$(function() {
    $('.menu_link').on('click', function() {
        event.preventDefault();
        var $this_item = $(this);
        var target_id = $(this).attr('href');
        $('.menu_target, .menu_item').removeClass('active');
        console.log($('[href="'+target_id+'"]'));
        $('[href="'+target_id+'"]').parent('.menu_item').addClass('active');
        $(target_id).addClass('active');
    });

    $('[data-action="js_toggle"]').on('click', function() {
        $(this).parent('.ui_toggle_container').toggleClass('ui_toggle_show');
    });

    // Add timezone
    $('#user_timezone').val(Intl.DateTimeFormat().resolvedOptions().timeZone);

    // Chart data
    var createTimeParts = function() {
        var timeparts = [];
        for (h=0; h<24; h++) {
            // for(m=0; m<6; m++) {
            //     var time_str = h.toString() + ':' + m.toString() + '0'
            //     timeparts.push({'time_str': time_str, 'count': 0})
            // }
            timeparts.push({'time_str': h.toString(), 'count': 0})
        }
        return timeparts
    }
    var getChartData = function() {
        var chart_data = {}
        $('.data_section').each(function() {
            var timeparts = createTimeParts()
            var log_button = $(this).attr('data-log-button');
            chart_data[log_button] = {
                'labels': [],
                'series': [],
                'hasData': false,
                'highestCount': 0
            }
            console.log(log_button);
            $(this).find('.log_item_container').each(function() {
                var this_time_str = $(this).find('.log_entry_time').text()
                $.each(timeparts, function(i, tp) {
                    var hour = this_time_str.substring(0,2)
                    var minutes = this_time_str.substring(3,5)
                    // Put 11.30 and 10.31 to 11h
                    var addToTimepart = false;
                    if (hour == tp['time_str'] &&  Number(minutes) <= 30) {
                        addToTimepart = true;
                    }
                    else if (Number(hour) == Number(tp['time_str'])-1 &&  Number(minutes) > 30) {
                        addToTimepart = true;
                    }

                    if (addToTimepart) {
                        tp['count']++;
                        chart_data[log_button]['hasData'] = true;
                        if (tp['count'] > chart_data[log_button]['highestCount']) {
                            chart_data[log_button]['highestCount'] = tp['count'];
                        }
                    }

                })
            });

            // Put it into a structure that is readable by chartis
            $.each(timeparts, function(i, tp) {
                chart_data[log_button]['labels'].push(tp['time_str']);
                chart_data[log_button]['series'].push(tp['count']);
            });
            // // The series must be a list in a list
            // var series_format = [chart_data[log_button]['series']];
            // chart_data[log_button]['series'] = series_format;

        });
        return chart_data
    }
    var chart_data = getChartData();
    var chart_options = {
        onlyInteger: true,
        width: '100%',
        height: '12rem',
        showLine: false,
        chartPadding: {
            top: 15,
            right: 10,
            bottom: 5,
            left: 10
          },
        axisY: {
            offset: 0,
            labelOffset: {
              x: 0,
              y: 5
            }
          },
        axisX: {
            labelOffset: {
                x: 0,
                y: 5
            }
        }
    }
    var getChart = function(chart_data) {
        var $el = $('<div></div>').addClass('chart');
        var label_height = '1.2rem'
        var steps = chart_data['highestCount'];
        var step_height = 100.0/(steps+1);
        // X -> Series
        var $axis_y_data = $('<div></div>').addClass('axis_y_data');
        for(i=steps; i>=0; i--) {
            var $row_container = '<div class="row_container" style="height: ' + step_height + '%;"><div class="row_label_outer"><div class="row_label_inner">' + i + '</div></div><div class="row_line_outer"><div class="row_line_inner"></div></div>'
            $axis_y_data.append($row_container);
        }
        $el.append($axis_y_data);
        // Y -> Labels
        var $axis_x_data = $('<div></div>').addClass('axis_x_data');
        var label_width = 100.0/chart_data['labels'].length;
        $(chart_data['labels']).each(function(i, data) {
            var this_bar_height = step_height * chart_data['series'][i];
            var $bar_container = '<div class="bar_container" style="width: ' + label_width + '%;"><div class="bar_outer" ><div class="bar_inner" style="height: ' + this_bar_height + '%;"></div></div><div class="bar_label_outer"><div class="bar_label_inner">' + i + '</div></div></div>';
            $axis_x_data.append($bar_container);
        });
        $el.append($axis_x_data);

        return $el

    };
    $.each(Object.keys(chart_data), function(i, id) {
        if (chart_data[id]['hasData']) {
            //new Chartist.Bar('#chart_' + id, chart_data[id], chart_options);
            $('#chart_' + id).find('.chart_placeholder').remove();
            $('#chart_' + id).append(getChart(chart_data[id]))
        }
    })
});