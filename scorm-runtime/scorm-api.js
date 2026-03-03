/**
 * SCORM 1.2 API — Runtime pour communiquer avec le LMS (Moodle, etc.)
 * OSER POUR INNOVER — Module 1 | v1.0
 * Détection API, suspend_data, lesson_status, score (cmi.core.*).
 */

(function (global) {
  'use strict';

  var findAPI = function (win) {
    var api = null;
    while (win && win !== win.parent) {
      win = win.parent;
    }
    if (win) {
      for (var i = 0; i < 8; i++) {
        var name = i === 0 ? 'API' : 'API_' + i;
        if (win[name]) {
          api = win[name];
          break;
        }
      }
    }
    return api;
  };

  var api = findAPI(global);

  var scorm = {
    isAvailable: function () {
      return api != null;
    },
    getValue: function (key) {
      if (!api) return '';
      return api.GetValue(key) || '';
    },
    setValue: function (key, value) {
      if (!api) return false;
      return api.SetValue(key, value);
    },
    getSuspendData: function () {
      return this.getValue('cmi.suspend_data');
    },
    setSuspendData: function (data) {
      return this.setValue('cmi.suspend_data', data);
    },
    commit: function () {
      if (!api) return false;
      return api.Commit('');
    },
    setLessonStatus: function (status) {
      if (!api) return false;
      return api.SetValue('cmi.core.lesson_status', status);
    },
    setScore: function (raw, min, max) {
      if (!api) return false;
      api.SetValue('cmi.core.score.raw', String(raw));
      api.SetValue('cmi.core.score.min', String(min != null ? min : 0));
      api.SetValue('cmi.core.score.max', String(max != null ? max : 100));
      return true;
    }
  };

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = scorm;
  } else {
    global.ScormAPI = scorm;
  }
})(typeof window !== 'undefined' ? window : this);
