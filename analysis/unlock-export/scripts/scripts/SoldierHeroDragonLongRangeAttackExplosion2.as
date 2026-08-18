package
{
   import flash.events.*;
   import flash.geom.*;
   
   [Embed(source="/_assets/assets.swf", symbol="symbol13973")]
   public class SoldierHeroDragonLongRangeAttackExplosion2 extends §extends const true§
   {
      
      internal var cRoot:Level;
      
      internal var damage:Number;
      
      internal var range:Number;
      
      public function SoldierHeroDragonLongRangeAttackExplosion2(param1:Point, param2:Level, param3:Number, param4:Number)
      {
         super();
         this.cRoot = param2;
         this.x = param1.x;
         this.y = param1.y;
         this.damage = param3;
         this.range = param4;
         this.stop();
         this.addEventListener(Event.ADDED_TO_STAGE,this.init,false,0,true);
      }
      
      public function init(param1:Event) : void
      {
         var _loc2_:EnemyCommon = null;
         this.play();
         for each(_loc2_ in this.cRoot.enemies)
         {
            if(_loc2_.isActive && !_loc2_.isDead && §_-Mm§.ellipseContains(this.x,this.y,_loc2_,this.range,this.cRoot.gameSettings.rangeRatio))
            {
               _loc2_.setDamage(this.damage,§_-Mm§.I_ARMOR);
               if(this.cRoot.game.gameHeroData.heroAshbite.skill5.level > 0)
               {
                  this.§_-Sj§(_loc2_);
               }
            }
         }
         this.cRoot.decals.addChild(new §_-r5§(new Point(this.x,this.y),this.cRoot));
      }
      
      public function pause() : void
      {
         this.stop();
      }
      
      public function unPause() : void
      {
         if(this.currentFrameLabel != "end")
         {
            play();
         }
      }
      
      public function onFrameUpdate() : void
      {
         if(this.currentFrameLabel == "end")
         {
            this.destroyThis();
         }
      }
      
      public function destroyThis() : void
      {
         this.parent.removeChild(this);
      }
      
      public function §_-Sj§(param1:EnemyCommon) : void
      {
         var _loc2_:int = int(this.cRoot.gameSettings.heroes.heroAshbite.reignOfFireSkill.damage[this.cRoot.game.gameHeroData.heroAshbite.skill5.level - 1]);
         var _loc3_:int = int(this.cRoot.gameSettings.heroes.heroAshbite.reignOfFireSkill.damageReloadTime[this.cRoot.game.gameHeroData.heroAshbite.skill5.level - 1]);
         var _loc4_:int = int(this.cRoot.gameSettings.heroes.heroAshbite.reignOfFireSkill.duration[this.cRoot.game.gameHeroData.heroAshbite.skill5.level - 1]);
         if(!param1.isActive)
         {
            return;
         }
         if(!param1.hasDebuff("SoldierHeroDragonBurnEnemyModifier"))
         {
            param1.§_-qI§(new SoldierHeroDragonBurnEnemyModifier(this.cRoot,1,param1,_loc2_,_loc3_,_loc4_));
         }
      }
   }
}

