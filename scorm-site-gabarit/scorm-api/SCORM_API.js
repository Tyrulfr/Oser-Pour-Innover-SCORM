/**
 * SCORM 2004 + 1.2 — wrapper LMS
 * Trouve API_1484_11 (2004) puis API (1.2), écrit les deux jeux CMI.
 */
(function (global) {
  'use strict';

  function searchWin(w) {
    while (w) {
      if (w.API_1484_11) return { api: w.API_1484_11, ver: '2004' };
      if (w.API && w.API !== scorm) return { api: w.API, ver: '12' };
      if (w === w.parent) break;
      w = w.parent;
    }
    return null;
  }

  function findAPI(win) {
    if (!win) return null;
    var found = searchWin(win);
    if (found) return found;
    if (win.opener) return searchWin(win.opener);
    return null;
  }

  var found = findAPI(typeof window !== 'undefined' ? window : global);
  var api = found ? found.api : null;
  var ver = found ? found.ver : '';
  var inited = false;
  var sessionStart = 0;
  var finished = false;

  function callGet(key) {
    if (!api) return '';
    try {
      if (typeof api.GetValue === 'function') return api.GetValue(key) || '';
      if (typeof api.LMSGetValue === 'function') return api.LMSGetValue(key) || '';
    } catch (e) {}
    return '';
  }

  function callSet(key, value) {
    if (!api) return false;
    try {
      var ok;
      if (typeof api.SetValue === 'function') ok = api.SetValue(key, String(value));
      else if (typeof api.LMSSetValue === 'function') ok = api.LMSSetValue(key, String(value));
      else return false;
      return ok !== 'false' && ok !== false;
    } catch (e) {}
    return false;
  }

  function callCommit() {
    if (!api) return false;
    try {
      if (typeof api.Commit === 'function') return api.Commit('') !== 'false';
      if (typeof api.LMSCommit === 'function') return api.LMSCommit('') !== 'false';
    } catch (e) {}
    return false;
  }

  function pad(n) {
    return (n < 10 ? '0' : '') + n;
  }

  function sessionSeconds() {
    if (!sessionStart) return 0;
    return Math.max(0, Math.floor((Date.now() - sessionStart) / 1000));
  }

  function format2004(sec) {
    var h = Math.floor(sec / 3600);
    var m = Math.floor((sec % 3600) / 60);
    var s = sec % 60;
    return 'PT' + h + 'H' + m + 'M' + s + 'S';
  }

  function format12(sec) {
    var h = Math.floor(sec / 3600);
    var m = Math.floor((sec % 3600) / 60);
    var s = sec % 60;
    return pad(Math.min(h, 9999)) + ':' + pad(m) + ':' + pad(s);
  }

  function writeSessionTime() {
    var sec = sessionSeconds();
    callSet('cmi.session_time', format2004(sec));
    callSet('cmi.core.session_time', format12(sec));
  }

  var scorm = {
    isAvailable: function () { return api != null; },
    version: function () { return ver; },
    getValue: function (key) { return callGet(key); },
    setValue: function (key, value) { return callSet(key, value); },
    getSuspendData: function () {
      return callGet('cmi.suspend_data') || callGet('cmi.core.suspend_data') || '';
    },
    setSuspendData: function (data) {
      var ok = callSet('cmi.suspend_data', data);
      callSet('cmi.core.suspend_data', data);
      return ok;
    },
    commit: function () {
      writeSessionTime();
      return callCommit();
    },
    setLessonStatus: function (status) {
      if (!api) return false;
      var completion = status;
      if (status === 'passed' || status === 'failed') completion = 'completed';
      callSet('cmi.completion_status', completion);
      callSet('cmi.core.lesson_status', status);
      return true;
    },
    setSuccess: function (status) {
      return callSet('cmi.success_status', status);
    },
    setProgress: function (ratio) {
      var n = Number(ratio);
      if (isNaN(n)) return false;
      if (n < 0) n = 0;
      if (n > 1) n = 1;
      return callSet('cmi.progress_measure', n.toFixed(4));
    },
    setLocation: function (loc) {
      callSet('cmi.location', loc);
      return callSet('cmi.core.lesson_location', loc);
    },
    setScore: function (raw, min, max) {
      if (!api) return false;
      var mn = min != null ? Number(min) : 0;
      var mx = max != null ? Number(max) : 100;
      var r = Number(raw);
      if (isNaN(r)) r = 0;
      var scaled = (mx - mn) !== 0 ? (r - mn) / (mx - mn) : 0;
      if (scaled < 0) scaled = 0;
      if (scaled > 1) scaled = 1;
      callSet('cmi.score.scaled', scaled.toFixed(4));
      callSet('cmi.score.raw', r);
      callSet('cmi.score.min', mn);
      callSet('cmi.score.max', mx);
      callSet('cmi.core.score.raw', r);
      callSet('cmi.core.score.min', mn);
      callSet('cmi.core.score.max', mx);
      return true;
    },
    setObjective: function (index, spec) {
      spec = spec || {};
      var p = 'cmi.objectives.' + index + '.';
      if (spec.id) callSet(p + 'id', spec.id);
      if (spec.completion) callSet(p + 'completion_status', spec.completion);
      if (spec.success) callSet(p + 'success_status', spec.success);
      if (spec.progress != null) callSet(p + 'progress_measure', spec.progress);
      if (spec.score != null) {
        callSet(p + 'score.raw', spec.score);
        callSet(p + 'score.min', 0);
        callSet(p + 'score.max', 100);
        callSet(p + 'score.scaled', (Number(spec.score) / 100).toFixed(4));
      }
    },
    recordInteraction: function (spec) {
      if (!api || !spec || !spec.id) return false;
      var n = parseInt(callGet('cmi.interactions._count') || '0', 10);
      if (isNaN(n)) n = 0;
      var p = 'cmi.interactions.' + n + '.';
      callSet(p + 'id', spec.id);
      callSet(p + 'type', spec.type || 'choice');
      if (spec.question) {
        callSet(p + 'description', spec.question);
      }
      if (spec.response != null) {
        callSet(p + 'learner_response', spec.response);
        callSet(p + 'student_response', spec.response);
      }
      if (spec.correct != null) {
        callSet(p + 'correct_responses.0.pattern', spec.correct);
      }
      if (spec.result) {
        callSet(p + 'result', spec.result);
      }
      if (spec.weighting != null) callSet(p + 'weighting', spec.weighting);
      if (spec.objective) callSet(p + 'objectives.0.id', spec.objective);
      var now = new Date();
      var iso = now.toISOString();
      callSet(p + 'timestamp', iso);
      callSet(p + 'time', pad(now.getHours()) + ':' + pad(now.getMinutes()) + ':' + pad(now.getSeconds()));
      return true;
    },
    lastError: function () {
      if (!api) return '';
      try {
        if (typeof api.GetLastError === 'function') return String(api.GetLastError());
        if (typeof api.LMSGetLastError === 'function') return String(api.LMSGetLastError());
      } catch (e) {}
      return '';
    },
    LMSInitialize: function () {
      if (inited) return 'true';
      if (!api) return 'false';
      try {
        var ok = 'true';
        if (typeof api.Initialize === 'function') ok = api.Initialize('') ? 'true' : 'false';
        else if (typeof api.LMSInitialize === 'function') ok = api.LMSInitialize('');
        if (ok === 'false') {
          var err = this.lastError();
          if (err !== '103' && err !== '101' && err !== '102') return 'false';
        }
      } catch (e) {}
      inited = true;
      sessionStart = Date.now();
      callSet('cmi.exit', 'suspend');
      callSet('cmi.core.exit', 'suspend');
      var status = callGet('cmi.completion_status') || callGet('cmi.core.lesson_status');
      if (!status || status === 'not attempted' || status === 'unknown') {
        callSet('cmi.completion_status', 'incomplete');
        callSet('cmi.core.lesson_status', 'incomplete');
        callSet('cmi.success_status', 'unknown');
      }
      return 'true';
    },
    LMSCommit: function () { return this.commit() ? 'true' : 'false'; },
    LMSFinish: function () {
      if (!api || finished) return;
      finished = true;
      writeSessionTime();
      callCommit();
      try {
        if (typeof api.Terminate === 'function') api.Terminate('');
        else if (typeof api.LMSFinish === 'function') api.LMSFinish('');
      } catch (e) {}
    },
    LMSGetValue: function (key) { return this.getValue(key); },
    LMSSetValue: function (key, value) { return this.setValue(key, value); }
  };

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = scorm;
  } else {
    global.ScormAPI = scorm;
    if (!global.API) global.API = scorm;
  }
})(typeof window !== 'undefined' ? window : this);
