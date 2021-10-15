var Imported = Imported || {};
Imported.miki_scaleFace = '1.0.0';

//=============================================================================
/*:
 * @plugindesc <miki_scaleFace>
 * Scales faces
 * @version 1.0.0
 * @author miki | github.com/porygon-tech
 * @site https://github.com/porygon-tech
 *
 * 
 * @param width
 * @text face width
 * @desc face width
 * @default 100
 * @type Number
 * 
 * @param height
 * @text face height
 * @desc face height
 * @default 100
 * @type Number
 *
 * @help
 * Plug and Play
 */


(function() {
	var _PARAMS = QPlus.getParams('<miki_scaleFace>', true);

	var _WIDTH  = _PARAMS['width'];
	var _HEIGHT = _PARAMS['height'];

	Window_Base.prototype.drawFace = function(faceName, faceIndex, x, y, width, height) {
	    width = width || Window_Base._faceWidth;
	    height = height || Window_Base._faceHeight;
	    var bitmap = ImageManager.loadFace(faceName);
	    var pw = Window_Base._faceWidth;
	    var ph = Window_Base._faceHeight;
	    var sw = Math.min(width, pw);
	    var sh = Math.min(height, ph);
	    var dx = Math.floor(x + Math.max(width - pw, 0) / 2);
	    var dy = Math.floor(y + Math.max(height - ph, 0) / 2);
	    var sx = faceIndex % 4 * pw + (pw - sw) / 2;
	    var sy = Math.floor(faceIndex / 4) * ph + (ph - sh) / 2;
	    var dw = 100; //your desired portrait width
		var dh = 100; //your desired portrait heith
		this.contents.blt(bitmap, sx, sy, sw, sh, dx, dy, dw, dh); //notice two more params
	};
})();