package
{
   import flash.geom.*;
   import flash.utils.*;
   
   public class §include function§ extends §_-td§
   {
      
      public var damagePointsMin:int;
      
      public var §_-XJ§:int;
      
      public var §in for break§:int;
      
      public var §dynamic for super§:int;
      
      public function §include function§(param1:Level, param2:int, param3:Enemy)
      {
         super(param1,param2,param3);
         this.§_-Tb§ = true;
      }
      
      override public function init() : void
      {
         this.setProperties();
         this.§dynamic for super§ = this.§in for break§ - 1;
      }
      
      override public function §_-NT§() : void
      {
         if(this.§dynamic for super§ < this.§in for break§)
         {
            ++this.§dynamic for super§;
            return;
         }
         var _loc1_:String = §_-Mm§.bloodToBleedMap[this.target.bloodClass];
         var _loc2_:Class = getDefinitionByName(_loc1_) as Class;
         var _loc3_:* = new _loc2_(new Point(this.target.x,this.target.y + this.target.yAdjust),0,this.cRoot);
         this.cRoot.bullets.addChild(_loc3_);
         _loc3_.scaleX = this.target.scaleX;
         Enemy(this.target).setDamage(this.getDamage(),§_-Mm§.I_ARMOR,null);
         this.§dynamic for super§ = 0;
      }
      
      override public function §throw with§(param1:Boolean) : void
      {
         if(param1)
         {
            this.§dynamic for break§();
         }
         this.destroyThis();
      }
      
      override public function §_-Yp§(param1:int) : void
      {
         this.level = param1;
         this.setProperties();
      }
      
      private function setProperties() : void
      {
         this.damagePointsMin = this.cRoot.gameSettings.heroes.heroCronan.deeplashesSkill.bleedDamage[this.cRoot.game.gameHeroData.heroCronan.skill4.level - 1];
         this.§_-XJ§ = this.cRoot.gameSettings.heroes.heroCronan.deeplashesSkill.bleedDamage[this.cRoot.game.gameHeroData.heroCronan.skill4.level - 1];
         this.durationTime = this.cRoot.gameSettings.heroes.heroCronan.deeplashesSkill.bleedDuration[this.cRoot.game.gameHeroData.heroCronan.skill4.level - 1] * this.cRoot.gameSettings.framesRate;
         this.§in for break§ = this.cRoot.gameSettings.framesRate;
         this.§throw for dynamic§();
         this.§continue else§ = 0;
      }
      
      protected function getDamage() : int
      {
         return (this.damagePointsMin + Math.ceil(Math.random() * (this.§_-XJ§ - this.damagePointsMin))) / 6;
      }
   }
}

