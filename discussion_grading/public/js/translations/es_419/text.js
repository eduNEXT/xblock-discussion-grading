
            (function(global){
                var DiscussionGradingI18N = {
                  init: function() {
                    

'use strict';
{
  const globals = this;
  const django = globals.django || (globals.django = {});

  
  django.pluralidx = function(n) {
    const v = (n != 1);
    if (typeof v === 'boolean') {
      return v ? 1 : 0;
    } else {
      return v;
    }
  };
  

  /* gettext library */

  django.catalog = django.catalog || {};
  
  const newcatalog = {
    "Button Text": "Texto del Bot\u00f3n",
    "Calculate Discussion Participation": "Calcular Participaci\u00f3n en la Discusi\u00f3n",
    "Defines the grading method to be used. When set to 'Minimum Participations', the learner will obtain the maximum score if the number of participations is greater than or equal to the number of participations required to pass, 0 otherwise. When set to 'Weighted Participations', the learner will obtain a score equal to the number of participations divided by the number of participations required to pass. The score is rounded to the nearest integer.": "Define el m\u00e9todo de calificaci\u00f3n a utilizar. Cuando se establece en 'M\u00ednimo de Participaciones', el estudiante obtendr\u00e1 la puntuaci\u00f3n m\u00e1xima si su n\u00famero de participaciones es mayor o igual al n\u00famero de participaciones requeridas para aprobar, 0 en caso contrario. Cuando se establece en 'Participaciones Ponderadas', el estudiante obtendr\u00e1 una puntuaci\u00f3n igual a su n\u00famero de participaciones dividido por el n\u00famero de participaciones requeridas para aprobar. La puntuaci\u00f3n se redondea al entero m\u00e1s cercano.",
    "Defines the instructions text to be displayed to the student.": "Define el texto de instrucciones que se mostrar\u00e1 al estudiante.",
    "Defines the number of participations required to pass. If the number of learner participations is greater than or equal to this value, the student will pass with the maximum score regardless of the grading method.": "Define el n\u00famero de participaciones requeridas para aprobar. Si el n\u00famero de participaciones del estudiante es mayor o igual a este valor, el estudiante aprobar\u00e1 con la puntuaci\u00f3n m\u00e1xima independientemente del m\u00e9todo de calificaci\u00f3n.",
    "Defines the number of points this problem is worth. By default, the problem is worth 10 points.": "Define el n\u00famero de puntos que vale este problema. Por defecto, el problema vale 10 puntos.",
    "Defines the number of times a student can attempt to calculate the grade. If the value is not set, infinite attempts are allowed.": "Define el n\u00famero de veces que un estudiante puede intentar calcular la calificaci\u00f3n. Si el valor no est\u00e1 establecido, se permiten intentos infinitos.",
    "Defines the text to be displayed on the button.": "Define el texto que se mostrar\u00e1 en el bot\u00f3n.",
    "Discussion Grading": "Calificaci\u00f3n de Discusi\u00f3n",
    "Discussion forum is not enabled. Please contact the course team.": "El foro de discusi\u00f3n no est\u00e1 habilitado. Por favor, contacta al equipo del curso.",
    "Display Name": "Nombre a Mostrar",
    "Forum stats for user not found. Follow the instructions for the course and try again.": "No se encontraron estad\u00edsticas del foro para el usuario. Sigue las instrucciones del curso e int\u00e9ntalo de nuevo.",
    "Grading Method": "M\u00e9todo de Calificaci\u00f3n",
    "Instructions Text": "Texto de Instrucciones",
    "Maximum Attempts": "Intentos M\u00e1ximos",
    "Minimum Participations": "M\u00ednimo de Participaciones",
    "Number of Participations": "N\u00famero de Participaciones",
    "Number of attempts taken by the student to calculate the grade.": "N\u00famero de intentos tomados por el estudiante para calcular la calificaci\u00f3n.",
    "Please press the button to calculate your grade according to the number of participations in the discussion forum.": "Por favor, presiona el bot\u00f3n para calcular tu calificaci\u00f3n de acuerdo al n\u00famero de participaciones en el foro de discusi\u00f3n.",
    "Problem Weight": "Peso del Problema",
    "Raw score": "Puntuaci\u00f3n Bruta",
    "Submission UUID": "UUID de la Entrega",
    "The display name for this component.": "El nombre a mostrar para este componente.",
    "The raw score for the assignment.": "La puntuaci\u00f3n bruta para la tarea.",
    "The submission UUID for the assignment.": "El UUID de la entrega para la tarea.",
    "Weighted Participations": "Participaciones Ponderadas",
    "You have made": "Has hecho",
    "You have reached the maximum number of attempts.": "Has alcanzado el n\u00famero m\u00e1ximo de intentos.",
    "Your score is:": "Tu puntuaci\u00f3n es:",
    "attempts to calculate the grading.": "intentos para calcular la calificaci\u00f3n."
  };
  for (const key in newcatalog) {
    django.catalog[key] = newcatalog[key];
  }
  

  if (!django.jsi18n_initialized) {
    django.gettext = function(msgid) {
      const value = django.catalog[msgid];
      if (typeof value === 'undefined') {
        return msgid;
      } else {
        return (typeof value === 'string') ? value : value[0];
      }
    };

    django.ngettext = function(singular, plural, count) {
      const value = django.catalog[singular];
      if (typeof value === 'undefined') {
        return (count == 1) ? singular : plural;
      } else {
        return value.constructor === Array ? value[django.pluralidx(count)] : value;
      }
    };

    django.gettext_noop = function(msgid) { return msgid; };

    django.pgettext = function(context, msgid) {
      let value = django.gettext(context + '\x04' + msgid);
      if (value.includes('\x04')) {
        value = msgid;
      }
      return value;
    };

    django.npgettext = function(context, singular, plural, count) {
      let value = django.ngettext(context + '\x04' + singular, context + '\x04' + plural, count);
      if (value.includes('\x04')) {
        value = django.ngettext(singular, plural, count);
      }
      return value;
    };

    django.interpolate = function(fmt, obj, named) {
      if (named) {
        return fmt.replace(/%\(\w+\)s/g, function(match){return String(obj[match.slice(2,-2)])});
      } else {
        return fmt.replace(/%s/g, function(match){return String(obj.shift())});
      }
    };


    /* formatting library */

    django.formats = {
    "DATETIME_FORMAT": "j \\d\\e F \\d\\e Y \\a \\l\\a\\s H:i",
    "DATETIME_INPUT_FORMATS": [
      "%d/%m/%Y %H:%M:%S",
      "%d/%m/%Y %H:%M:%S.%f",
      "%d/%m/%Y %H:%M",
      "%d/%m/%y %H:%M:%S",
      "%d/%m/%y %H:%M:%S.%f",
      "%d/%m/%y %H:%M",
      "%Y-%m-%d %H:%M:%S",
      "%Y-%m-%d %H:%M:%S.%f",
      "%Y-%m-%d %H:%M",
      "%Y-%m-%d"
    ],
    "DATE_FORMAT": "j \\d\\e F \\d\\e Y",
    "DATE_INPUT_FORMATS": [
      "%d/%m/%Y",
      "%d/%m/%y",
      "%Y-%m-%d"
    ],
    "DECIMAL_SEPARATOR": ",",
    "FIRST_DAY_OF_WEEK": 1,
    "MONTH_DAY_FORMAT": "j \\d\\e F",
    "NUMBER_GROUPING": 3,
    "SHORT_DATETIME_FORMAT": "d/m/Y H:i",
    "SHORT_DATE_FORMAT": "d/m/Y",
    "THOUSAND_SEPARATOR": "\u00a0",
    "TIME_FORMAT": "H:i",
    "TIME_INPUT_FORMATS": [
      "%H:%M:%S",
      "%H:%M:%S.%f",
      "%H:%M"
    ],
    "YEAR_MONTH_FORMAT": "F \\d\\e Y"
  };

    django.get_format = function(format_type) {
      const value = django.formats[format_type];
      if (typeof value === 'undefined') {
        return format_type;
      } else {
        return value;
      }
    };

    /* add to global namespace */
    globals.pluralidx = django.pluralidx;
    globals.gettext = django.gettext;
    globals.ngettext = django.ngettext;
    globals.gettext_noop = django.gettext_noop;
    globals.pgettext = django.pgettext;
    globals.npgettext = django.npgettext;
    globals.interpolate = django.interpolate;
    globals.get_format = django.get_format;

    django.jsi18n_initialized = true;
  }
};


                  }
                };
                DiscussionGradingI18N.init();
                global.DiscussionGradingI18N = DiscussionGradingI18N;
            }(this));
        