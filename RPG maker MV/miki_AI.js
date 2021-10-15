//=============================================================================
// miki_AI
//=============================================================================

var Imported = Imported || {};

if (!Imported.QABS || !QPlus.versionCheck(Imported.QABS, '1.7.0')) {
  alert('Error: miki_AI requires QABS 1.7.0 or newer to work.');
  throw new Error('Error: miki_AI requires QABS 1.7.0 or newer to work.');
}

Imported.miki_AI = '1.0.0';

//=============================================================================
/*:
 * @plugindesc <miki_AI>
 * QABS addon: enemy AI
 * @version 1.0.0
 * @author miki | github.com/porygon-tech
 * @site https://github.com/porygon-tech
 *
 * @requires QABS
 * 
 * @param AAA
 * @text Use AAA
 * @desc (ALPHA VERSION)
 * 
 * @default false
 * @type boolean
 *
 * @help
 * ...
 */


(function() {

  Game_Event.prototype.validAI = function() {
    // if added new AI types, expand here with its name so the
    // updateAI will run
    return this._aiType === "simple", "coward", "predator";
  };

  Game_Event.prototype.updateAI = function(type) {
    if (type === 'simple') {
      return this.updateAISimple();
    } else if (type === 'coward') {
      return this.updateAICoward();
    }
    // to add more AI types, alias this function
    // and do something similar to above
  };

// ============================================= 
//|                 COWARD                      |
// ============================================= 

  Game_Event.prototype.updateAICoward = function() {
    var bestTarget = this.bestTarget();
    if (!bestTarget) return;
    var targetId = bestTarget.charaId();
    if (!this.AICowardInRange(bestTarget)) return;
    this.AICowardAction(bestTarget, this.AICowardGetAction(bestTarget));
  };

  Game_Event.prototype.AICowardInRange = function(bestTarget) {
    var targetId = bestTarget.charaId();
    if (this.isTargetInRange(bestTarget)) {
      this._agro.placeInCombat();
      if (!this._agro.has(targetId)) {
        console.log("!this._agro.has(targetId)")
        this._aiWait = QABS.aiWait;
        this.addAgro(targetId);
        if (this._aiPathfind) {
          this.clearPathfind();
        }
      }
      if (this._endWait) {
        //console.log("this._endWait")
        this.removeWaitListener(this._endWait);
        this._endWait = null;
      }
      return true;
    } else {
      if (this._agro.has(targetId)) {
        if (this._aiPathfind) {
          this.clearPathfind();
        }
        this._endWait = this.wait(90).then(function() {
          this._endWait = null;
          this.endCombat();
          console.log("this.endCombat()")
        }.bind(this));
        this.removeAgro(targetId);
      }
      if (this._endWait && this.canMove()) {
        //this.moveTowardCharacter(bestTarget);
      }
      return false;
    }
    return false;
  };

  Game_Event.prototype.AICowardGetAction = function(bestTarget) {
    var bestAction = null;
    if (this._aiWait >= QABS.aiWait) {
      this.turnTowardCharacter(bestTarget);
      bestAction = QABSManager.bestAction(this.charaId());
      this._aiWait = 0;
    } else {
      this._aiWait++;
    }
    return bestAction;
  };

  Game_Event.prototype.AICowardAction = function(bestTarget, bestAction) {
    if (bestAction) {
      console.log("in range to attack")
      var skill = this.useSkill(bestAction);
      if (skill) skill._target = bestTarget;
    } else if (this.canMove()) {
      if (this._aiPathfind) {
      console.log("this._aiPathfind")
        var dx = bestTarget.cx() - this.cx();
        var dy = bestTarget.cy() - this.cy();
        var mw = this.collider('collision').width + bestTarget.collider('collision').width;
        var mh = this.collider('collision').height + bestTarget.collider('collision').height;
        if (Math.abs(dx) <= mw && Math.abs(dy) <= mh) {
          this.clearPathfind();
          this.moveTowardCharacter(bestTarget);
        } else if (this.battler().hp < 0.5 * this.battler().mhp) {
        // chase player, or escape if HP is low
          console.log("coward mode on")
          this.moveAwayFromCharacter(bestTarget);
        } else {
          this.initChase(bestTarget.charaId());
        }
      } else {
        this.moveTowardCharacter(bestTarget);
      }
    }
  };

// ============================================= 
})();
