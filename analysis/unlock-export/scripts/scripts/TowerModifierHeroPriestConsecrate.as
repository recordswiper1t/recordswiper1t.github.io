package
{
   [Embed(source="/_assets/assets.swf", symbol="symbol14487")]
   public class TowerModifierHeroPriestConsecrate extends §_-GY§
   {
      
      private var §_-ED§:int;
      
      public function TowerModifierHeroPriestConsecrate(param1:Level, param2:int, param3:§_-5u§)
      {
         super(param1,param2,param3);
         this.mouseChildren = false;
         this.mouseEnabled = false;
      }
      
      override public function pause() : void
      {
         this.stop();
      }
      
      override public function unPause() : void
      {
         this.play();
      }
      
      override public function init() : void
      {
         this.setProperties();
         this.tower.§true const static§ = this.§_-ED§;
         this.§throw for dynamic§();
      }
      
      override public function §throw with§() : void
      {
         this.tower.§_-3m§.splice(this.tower.§_-3m§.indexOf(this),1);
         this.tower.§true const static§ = 0;
         this.destroyThis();
      }
      
      override public function §_-Yp§(param1:int) : void
      {
         this.level = param1;
         this.setProperties();
         this.tower.§true const static§ = this.§_-ED§;
      }
      
      override public function §dynamic for break§() : void
      {
         this.destroyThis();
      }
      
      override public function §throw for dynamic§() : void
      {
         this.x = this.tower.x;
         this.y = this.tower.y + this.tower.§_-6d§;
         this.cRoot.entities.addChild(this);
      }
      
      private function setProperties() : void
      {
         var _loc1_:Object = this.cRoot.gameSettings.heroes.heroDierdre.consecrateSkill;
         this.§_-ED§ = _loc1_.bonusDamage[this.level - 1];
         this.durationTime = _loc1_.duration[this.level - 1] * this.cRoot.gameSettings.framesRate;
         this.§continue else§ = 0;
      }
   }
}

