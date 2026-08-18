package
{
   import flash.geom.*;
   
   [Embed(source="/_assets/assets.swf", symbol="symbol13930")]
   public class §_-WZ§ extends §extends const true§
   {
      
      internal var damage:int;
      
      internal var damageReloadTime:int;
      
      internal var §_-B2§:int;
      
      internal var isActive:Boolean;
      
      internal var callback:Function;
      
      internal var §_-Io§:Number = 0;
      
      internal var duration:Number;
      
      internal var cRoot:Level;
      
      internal var §_-MY§:§catch get§;
      
      public function §_-WZ§(param1:Level, param2:Point, param3:int, param4:int, param5:*)
      {
         super();
         this.cRoot = param1;
         this.x = param2.x;
         this.y = param2.y;
         this.§_-B2§ = 0;
         this.damageReloadTime = 2;
         this.duration = param4;
         this.damage = param3 * this.damageReloadTime / param4;
         this.§_-MY§ = new §catch get§(this.x,this.y);
         this.cRoot.decals.addChild(this.§_-MY§);
         this.isActive = true;
         this.callback = param5;
      }
      
      public function pause() : void
      {
         this.stop();
      }
      
      public function unPause() : void
      {
         this.play();
      }
      
      public function onFrameUpdate() : void
      {
         var _loc1_:EnemyCommon = null;
         if(this.currentFrame == 29)
         {
            this.destroyThis();
            return;
         }
         if(this.currentFrame == 19)
         {
            this.cRoot.decals.addChild(new §_-r5§(new Point(this.x,this.y),this.cRoot));
         }
         ++this.§_-B2§;
         if(this.§_-B2§ > this.damageReloadTime)
         {
            for each(_loc1_ in this.cRoot.enemies)
            {
               if(!_loc1_.isFlying && _loc1_.isActive && !_loc1_.isDead && §_-Mm§.ellipseContains(this.x,this.y,_loc1_,120 / 1.28,this.cRoot.gameSettings.rangeRatio))
               {
                  _loc1_.setDamage(this.damage,§_-Mm§.I_ARMOR);
                  if(this.cRoot.game.gameHeroData.heroAshbite.skill5.level > 0)
                  {
                     this.§_-Sj§(_loc1_);
                  }
               }
            }
            this.§_-B2§ = 0;
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

