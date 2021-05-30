function doFormat (x, pattern, mask) {
  var strippedValue = x.replace(/[^0-9]/g, '')
  var chars = strippedValue.split('')
  var count = 0

  var formatted = ''
  for (var i = 0; i < pattern.length; i++) {
    const c = pattern[i]
    if (chars[count]) {
      if (/\*/.test(c)) {
        formatted += chars[count]
        count++
      } else {
        formatted += c
      }
    } else if (mask) {
      if (mask.split('')[i]) { formatted += mask.split('')[i] }
    }
  }
  return formatted
}

document.querySelectorAll('[data-mask]').forEach(function (e) {
  function format (elem) {
    const val = doFormat(elem.value, elem.getAttribute('data-format'))
    elem.value = doFormat(elem.value, elem.getAttribute('data-format'), elem.getAttribute('data-mask'))

    if (elem.createTextRange) {
      var range = elem.createTextRange()
      range.move('character', val.length)
      range.select()
    } else if (elem.selectionStart) {
      elem.focus()
      elem.setSelectionRange(val.length, val.length)
    }
  }
  e.addEventListener('keyup', function () {
    format(e)
  })
  e.addEventListener('keydown', function () {
    format(e)
  })
  format(e)
})
