package
{
   import §_-aW§.*;
   import flash.geom.*;
   
   [Embed(source="/_assets/assets.swf", symbol="symbol13334")]
   public class §override use§ extends §extends const true§
   {
      
      internal var level:int;
      
      internal var cRoot:Level;
      
      internal var isActive:Boolean;
      
      internal var §_-iG§:Boolean;
      
      internal var durationTime:int;
      
      internal var damage:int;
      
      internal var currentEnemies:int;
      
      internal var maxEnemies:int;
      
      internal var §for const try§:int;
      
      internal var §case const try§:int;
      
      internal var §dynamic const§:int;
      
      internal var §null for set§:int;
      
      internal var c:int;
      
      internal var §_-GF§:int;
      
      internal var countTentacles:int = 0;
      
      public function §override use§(param1:Point, param2:Level, param3:int)
      {
         super();
         addFrameScript(22,this.frame23,31,this.frame32);
         this.cRoot = param2;
         this.level = param3;
         this.x = param1.x;
         this.y = param1.y;
         this.level = param3;
         this.isActive = false;
         this.§_-iG§ = false;
         this.durationTime = this.cRoot.gameSettings.heroes.heroCaptain.krakenDuration * this.cRoot.gameSettings.framesRate;
         this.damage = this.cRoot.gameSettings.heroes.heroCaptain.krakenDamage;
         this.maxEnemies = this.cRoot.gameSettings.heroes.heroCaptain.krakenMaxEnemies + this.cRoot.game.gameHeroData.heroCaptain.skill5.level * this.cRoot.gameSettings.heroes.heroCaptain.krakenMaxEnemiesIncrement;
         this.§dynamic const§ = this.cRoot.gameSettings.heroes.heroCaptain.krakenAttackRange;
         this.§null for set§ = this.§dynamic const§ * this.cRoot.gameSettings.rangeRatio;
         this.currentEnemies = 0;
         this.c = 0;
         this.§for const try§ = 10;
         this.§case const try§ = 0;
      }
      
      public function onFrameUpdate() : void
      {
         var _loc2_:EnemyCommon = null;
         if(this.currentFrameLabel == "loop" && !this.§_-iG§)
         {
            this.isActive = true;
         }
         if(this.currentFrameLabel == " fadeOutEnd" && this.§_-iG§)
         {
            this.§_-l0§();
         }
         ++this.§_-GF§;
         if(this.§_-GF§ >= this.durationTime && !this.§_-iG§)
         {
            this.playAnimationEnd();
         }
         if(this.§_-iG§)
         {
            ++this.countTentacles;
         }
         if(this.countTentacles == 15)
         {
            this.gotoAndPlay("fadeOut");
         }
         ++this.c;
         if(!this.isActive)
         {
            return;
         }
         if(this.§_-iG§)
         {
            return;
         }
         if(this.§case const try§ < this.§for const try§)
         {
            ++this.§case const try§;
            return;
         }
         var _loc1_:§dynamic const in§ = new §dynamic const in§(this.x - this.§dynamic const§ / 2,this.y - this.§null for set§ / 2,this.§dynamic const§,this.§null for set§);
         for each(_loc2_ in this.cRoot.enemies)
         {
            if(_loc2_.isActive && _loc2_.§dynamic const for§ && !_loc2_.isBoss && !_loc2_.isFlying && _loc1_.containsPoint(new Point(_loc2_.x,_loc2_.y)))
            {
               if(!_loc2_.hasDebuff("EnemyModifierWaterKraken"))
               {
                  if(this.currentEnemies <= this.maxEnemies)
                  {
                     _loc2_.§_-nS§(this.damage,this.durationTime - this.c + 10,10,this.level);
                     ++this.currentEnemies;
                  }
               }
               _loc2_.§_-qI§(new EnemyModifierSlowKraken(this.cRoot,this.level,_loc2_));
            }
         }
         this.§case const try§ = 0;
      }
      
      public function playAnimationEnd() : void
      {
         var _loc1_:EnemyCommon = null;
         this.§_-iG§ = true;
         for each(_loc1_ in this.cRoot.enemies)
         {
            _loc1_.§_-NE§("EnemyModifierWaterKraken");
            _loc1_.§_-NE§("EnemyModifierSlowKraken");
         }
      }
      
      public function pause() : void
      {
         this.stop();
      }
      
      public function unPause() : void
      {
         switch(this.currentFrameLabel)
         {
            case "loop":
               this.gotoAndPlay("loop");
               break;
            case "fadeOutEnd":
               break;
            default:
               this.play();
         }
      }
      
      public function §_-l0§() : void
      {
         this.destroyThis();
      }
      
      protected function destroyThis() : void
      {
         this.parent.removeChild(this);
      }
      
      internal function frame23() : *
      {
         gotoAndPlay("loop");
      }
      
      internal function frame32() : *
      {
         stop();
      }
   }
}

