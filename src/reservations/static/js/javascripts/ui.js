// Generated by CoffeeScript 1.12.6
(function() {
  var AjaxModel, Calendar, Holidays, Month, Reservation,
    extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
    hasProp = {}.hasOwnProperty,
    indexOf = [].indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; };

  window.App = {
    monthData: [],
    defaults: {},
    init: function() {
      this.calendar = new Calendar($("#calendar"));
      new Month(this.calendar.month + 1, this.calendar.year);
      new Reservation(this.calendar.year);
      return new Holidays(this.calendar.year);
    },
    renderTime: function() {
      var hh, nn, now;
      now = new Date();
      hh = now.getHours();
      nn = "0" + now.getMinutes();
      $('.time').html(hh + ":" + nn.substr(-2));
      return setTimeout(App.renderTime, 500);
    }
  };

  AjaxModel = (function() {
    AjaxModel.prototype.url = "model_url";

    function AjaxModel(data) {
      if (data == null) {
        data = null;
      }
      $.ajax({
        url: this.url,
        data: data,
        success: this.successHandler,
        error: this.errorHandler
      });
    }

    AjaxModel.prototype.successHandler = function(data) {
      return this.data = data;
    };

    AjaxModel.prototype.errorHandler = function(data) {
      console.log("ERROR during fetching " + this.url);
      return console.log(data);
    };

    return AjaxModel;

  })();

  Holidays = (function(superClass) {
    extend(Holidays, superClass);

    Holidays.prototype.url = "holidays";

    function Holidays(year1) {
      var data;
      this.year = year1;
      Holidays.__super__.constructor.call(this, data = {
        year: this.year
      });
    }

    Holidays.prototype.successHandler = function(data) {
      var elem, k, len, lengthBefore, ref;
      this.data = data;
      lengthBefore = App.calendar._holidays.length;
      ref = data.holidays;
      for (k = 0, len = ref.length; k < len; k++) {
        elem = ref[k];
        elem.date = new Date(elem.date * 1000);
        App.calendar.addHoliday(elem);
      }
      if (App.calendar._holidays.length !== lengthBefore) {
        return App.calendar.render();
      }
    };

    return Holidays;

  })(AjaxModel);

  Month = (function() {
    Month.prototype.data = {};

    function Month(month1, year1) {
      var that;
      this.month = month1;
      this.year = year1;
      that = this;
      $.ajax({
        url: 'month/' + this.month + '/' + this.year,
        success: function(data) {
          return that.successHandler.call(that, data);
        },
        error: this.errorHandler
      });
    }

    Month.prototype.successHandler = function(data) {
      var date, elem, k, len;
      for (k = 0, len = data.length; k < len; k++) {
        elem = data[k];
        date = new Date(elem.fields.date * 1000);
        date.setHours(0);
        App.monthData[date] = elem.fields;
      }
      return App.calendar.render();
    };

    Month.prototype.errorHandler = function(data) {
      console.log("ERROR during fetching user data!");
      return console.log(data);
    };

    return Month;

  })();

  Reservation = (function() {
    function Reservation(year1) {
      this.year = year1;
      $.ajax({
        url: 'reservation',
        data: {
          year: this.year
        },
        success: this.successHandler,
        error: this.errorHandler
      });
    }

    Reservation.prototype.successHandler = function(data) {
      var elem, k, len, lengthBefore, ref;
      this.data = data;
      lengthBefore = App.calendar._reservations.length;
      ref = data.reservations;
      for (k = 0, len = ref.length; k < len; k++) {
        elem = ref[k];
        elem.date = new Date(elem.date * 1000);
        App.calendar.addReservation(elem);
      }
      if (App.calendar._reservations.length !== lengthBefore) {
        return App.calendar.render();
      }
    };

    Reservation.prototype.errorHandler = function(data) {
      console.log("ERROR during fetching user reservations!");
      return console.log(data);
    };

    return Reservation;

  })();

  Calendar = (function() {
    function Calendar(elem1) {
      var now;
      this.elem = elem1;
      this.tableHeader = this.elem.find('> thead:last');
      this.tableBody = this.elem.find('> tbody:last');
      now = new Date();
      this.month = now.getMonth();
      this.year = now.getFullYear();
      this.modalInfo = $('#modal-info');
      this.modalDetail = $('#modal-detail-form');
    }

    Calendar.prototype.updateReservationDay = function(reservationDay) {
      var date;
      date = new Date(reservationDay.fields.date * 1000);
      date.setHours(0);
      return App.monthData[date] = reservationDay.fields;
    };

    Calendar.prototype._reservations = [];

    Calendar.prototype._holidays = [];

    Calendar.prototype.addReservation = function(date) {
      return this._reservations.push(date);
    };

    Calendar.prototype.addHoliday = function(holiday) {
      return this._holidays.push(holiday);
    };

    Calendar.prototype.removeReservation = function(reservation_id) {
      var index, remove, results;
      index = 0;
      results = [];
      while (index < this._reservations.length) {
        remove = this._reservations[index].id === reservation_id;
        if (remove) {
          results.push(this._reservations.splice(index, 1));
        } else {
          results.push(index += 1);
        }
      }
      return results;
    };

    Calendar.prototype.inReservations = function(day, month, year) {
      var elem, k, len, ref;
      ref = this._reservations;
      for (k = 0, len = ref.length; k < len; k++) {
        elem = ref[k];
        if (elem.date.getDate() === day && elem.date.getMonth() === month && elem.date.getFullYear() === year) {
          return true;
        }
      }
      return false;
    };

    Calendar.prototype.getReservations = function(day, month, year) {
      var elem, k, len, out, ref;
      out = [];
      ref = this._reservations;
      for (k = 0, len = ref.length; k < len; k++) {
        elem = ref[k];
        if (elem.date.getDate() === day && elem.date.getMonth() === month && elem.date.getFullYear() === year) {
          out.push(elem);
        }
      }
      return out;
    };

    Calendar.prototype.daysInMonth = function(month, year) {
      return new Date(year, month, 0).getDate();
    };

    Calendar.prototype.makeReservation = function(mon, dayOfMonth, extraData) {
      var data, that;
      if (extraData == null) {
        extraData = null;
      }
      that = this;
      data = {
        year: mon.getFullYear(),
        month: mon.getMonth() + 1,
        day: dayOfMonth,
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
      };
      return $.ajax({
        url: 'reservation',
        type: 'POST',
        data: $.param(data) + (extraData ? "&" + extraData : ""),
        success: function(data) {
          return that.reservationSuccess.call(that, data);
        },
        error: function(data) {
          return that.reservationError.call(that, data);
        }
      });
    };

    Calendar.prototype.renderDays = function(mon) {
      var _html, currdate, dayOfMonth, dayReservations, daysInMonth, divClass, fdom, first, holiday, i, id, in_future, k, l, last, len, len1, m, message, mwks, now, ref, ref1, reservation, results, spots_free, that, weekDay;
      this.tableBody.empty();
      now = new Date();
      fdom = mon.getDay() - 1;
      if (fdom < 0) {
        fdom = 7 + fdom;
      }
      mwks = 6;
      dayOfMonth = 0;
      first = 0;
      last = 0;
      i = 0;
      daysInMonth = this.daysInMonth(mon.getMonth() + 1, mon.getFullYear());
      results = [];
      while (i >= last) {
        _html = "";
        for (weekDay = k = 0, ref = Data.weekDays.length; 0 <= ref ? k < ref : k > ref; weekDay = 0 <= ref ? ++k : --k) {
          divClass = [];
          message = "";
          id = "";
          currdate = new Date(mon.getFullYear(), mon.getMonth(), dayOfMonth + 1);
          if (first >= daysInMonth) {
            dayOfMonth = 0;
          } else if ((dayOfMonth > 0 && first > 0) || weekDay === fdom) {
            dayOfMonth += 1;
            first += 1;
          }
          if (1 * dayOfMonth === daysInMonth) {
            last = daysInMonth;
          }
          ref1 = this._holidays;
          for (l = 0, len = ref1.length; l < len; l++) {
            holiday = ref1[l];
            if (holiday.date.getTime() === currdate.getTime()) {
              divClass.push("holiday");
              message = holiday.name;
            }
          }
          in_future = function() {
            if ((dayOfMonth > now.getDate() && now.getMonth() === mon.getMonth() && now.getFullYear() === mon.getFullYear()) || now.getMonth() < mon.getMonth() || now.getFullYear() < mon.getFullYear()) {
              return true;
            }
            return false;
          };
          if (divClass.length === 0) {
            if (this.inReservations(dayOfMonth, mon.getMonth(), mon.getFullYear())) {
              divClass.push("reservation");
            }
            if (dayOfMonth === now.getDate() && now.getMonth() === mon.getMonth() && now.getFullYear() === mon.getFullYear()) {
              divClass.push("today");
            } else if (weekDay === 5 || weekDay === 6) {
              divClass.push("weekend");
            } else if (in_future()) {
              if (!App.monthData[currdate] || App.monthData[currdate].spots_free > 0) {
                divClass.push("future");
              }
            } else {
              divClass.push("past");
            }
          }
          id = "cell_" + i + "" + weekDay + "" + (dayOfMonth > 10 ? dayOfMonth : "0" + dayOfMonth);
          if (dayOfMonth === 0) {
            _html += '<td>&nbsp;</td>';
          } else if (message.length > 0) {
            _html += '<td class="' + divClass.join(" ") + '" id="' + id + '">' + dayOfMonth;
            _html += '<br/><span class="content">' + message + '</span></td>';
          } else {
            _html += '<td class="' + divClass.join(" ") + '" id="' + id + '">' + dayOfMonth;
            dayReservations = this.getReservations(dayOfMonth, mon.getMonth(), mon.getFullYear());
            if (indexOf.call(divClass, "future") >= 0 && (!App.defaults.reservations_limit || dayReservations.length < App.defaults.reservations_limit)) {
              _html += '<br/><ul class="day-actions"><li><button class="btn btn-primary btn-reserve">' + Data.label.reserve + '</button></li></ul>';
            }
            if (indexOf.call(divClass, "reservation") >= 0 && in_future()) {
              for (m = 0, len1 = dayReservations.length; m < len1; m++) {
                reservation = dayReservations[m];
                _html += '<br/><ul class="day-actions"><li><button db-id="' + reservation.id + '" class="btn btn-warning btn-unreserve">[' + reservation.short_desc + "] " + Data.label.cancel + '</button></li></ul>';
              }
            }
            if ((indexOf.call(divClass, "reservation") >= 0 || indexOf.call(divClass, "future") >= 0) && in_future()) {
              if (App.monthData[currdate]) {
                spots_free = App.monthData[currdate].spots_free;
              } else {
                spots_free = App.defaults.spots_free;
              }
              _html += '<div class="info">' + spots_free + ' ' + Data.txt.free_spots + '</div></td>';
            }
          }
        }
        _html = "<tr>" + _html + "</tr>";
        this.tableBody.append(_html);
        that = this;
        $('.btn-reserve').unbind('click').bind('click', function() {
          dayOfMonth = $(this).closest("td").attr("id").substr(-2);
          if (App.defaults.get_extra_data) {
            that.clearErrors('');
            that.modalDetail.modal();
            return $('.btn-primary', that.modalDetail).unbind('click').bind('click', function() {
              return that.makeReservation(mon, dayOfMonth, $("form", that.modalDetail).serialize());
            });
          } else {
            return that.makeReservation(mon, dayOfMonth);
          }
        });
        $('.btn-unreserve').unbind('click').bind('click', function() {
          var params;
          dayOfMonth = $(this).closest("td").attr("id").substr(-2);
          params = {
            id: $(this).attr("db-id")
          };
          return $.ajax({
            url: 'reservation?' + $.param(params),
            type: 'DELETE',
            headers: {
              "X-CSRFToken": $("input[name=csrfmiddlewaretoken]").val()
            },
            success: function(data) {
              return that.unreservationSuccess.call(that, data);
            },
            error: function(data) {
              return that.unreservationError.call(that, data);
            }
          });
        });
        results.push(i += 1);
      }
      return results;
    };

    Calendar.prototype.clearErrors = function(defaultClass) {
      var element, k, l, len, len1, ref, ref1, results;
      if (defaultClass == null) {
        defaultClass = "success";
      }
      ref = document.getElementsByClassName("control-group");
      for (k = 0, len = ref.length; k < len; k++) {
        element = ref[k];
        element.classList.remove("error");
        if (defaultClass) {
          element.classList.add(defaultClass);
        }
      }
      ref1 = document.getElementsByClassName("help-inline");
      results = [];
      for (l = 0, len1 = ref1.length; l < len1; l++) {
        element = ref1[l];
        results.push(element.innerHTML = "");
      }
      return results;
    };

    Calendar.prototype.renderError = function(fieldName, text) {
      var container, error_desc, field;
      field = document.getElementById("id_" + fieldName);
      container = field.parentNode.parentNode;
      error_desc = container.getElementsByClassName("help-inline")[0];
      error_desc.innerHTML = text;
      container.classList.remove("success");
      return container.classList.add("error");
    };

    Calendar.prototype.reservationSuccess = function(data) {
      var error, k, len, ref, reservation, results;
      if ("errors" in data) {
        this.clearErrors();
        ref = data.errors;
        results = [];
        for (k = 0, len = ref.length; k < len; k++) {
          error = ref[k];
          results.push(this.renderError(error[0], error[1]));
        }
        return results;
      } else {
        this.updateReservationDay(data.reservation_day);
        reservation = data.reservation;
        reservation.date = new Date(reservation.date * 1000);
        this.addReservation(reservation);
        this.modalDetail.modal('hide');
        return App.calendar.render();
      }
    };

    Calendar.prototype.reservationError = function(data) {
      $('h3', this.modalInfo).text(Data.txt.operation_forbidden);
      $('p', this.modalInfo).text(data.responseText);
      return this.modalInfo.modal('show');
    };

    Calendar.prototype.unreservationSuccess = function(data) {
      this.updateReservationDay(data.reservation_day);
      this.removeReservation(data.id);
      return App.calendar.render();
    };

    Calendar.prototype.unreservationError = function(data) {
      $('h3', this.modalInfo).text(Data.txt.operation_forbidden);
      $('p', this.modalInfo).text(data.responseText);
      return this.modalInfo.modal('show');
    };

    Calendar.prototype.renderDaysOfWeek = function() {
      var _html, j, k, ref;
      this.tableHeader.empty();
      for (j = k = 0, ref = Data.weekDays.length; 0 <= ref ? k < ref : k > ref; j = 0 <= ref ? ++k : --k) {
        _html += "<th>" + Data.weekDays[j] + "</th>";
      }
      _html = "<tr>" + _html + "</tr>";
      return this.tableHeader.append(_html);
    };

    Calendar.prototype.render = function(mm, yy) {
      var mon, now, nxt, prv, yn, yp;
      if (mm == null) {
        mm = null;
      }
      if (yy == null) {
        yy = null;
      }
      now = new Date();
      if (mm !== null && yy !== null) {
        this.month = mm;
        this.year = yy;
      }
      mm = this.month;
      yy = this.year;
      mon = new Date(yy, mm, 1);
      yp = mon.getFullYear();
      yn = mon.getFullYear();
      $('#last').removeClass('disabled');
      if (now.getMonth() > mm - 1 && now.getFullYear() === yy) {
        $('#last').addClass('disabled');
      }
      prv = new Date(yp, mm - 1, 1);
      nxt = new Date(yn, mm + 1, 1);
      $('.year').html(mon.getFullYear());
      $('.month').html(Data.months[mon.getMonth()]);
      this.renderDaysOfWeek();
      this.renderDays(mon);
      $('#last').unbind('click').bind('click', function() {
        if (!$(this).hasClass("disabled")) {
          App.calendar.render(prv.getMonth(), prv.getFullYear());
          return new Month(prv.getMonth() + 1, prv.getFullYear());
        }
      });
      $('#current').unbind('click').bind('click', function() {
        return App.calendar.render(now.getMonth(), now.getFullYear());
      });
      return $('#next').unbind('click').bind('click', function() {
        App.calendar.render(nxt.getMonth(), nxt.getFullYear());
        return new Month(nxt.getMonth() + 1, nxt.getFullYear());
      });
    };

    return Calendar;

  })();

  $(document).ready(function() {
    App.init();
    App.calendar.render();
    return App.renderTime();
  });

}).call(this);
