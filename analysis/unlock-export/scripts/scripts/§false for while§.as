package
{
   import flash.display.MovieClip;
   import flash.events.*;
   
   [Embed(source="/_assets/assets.swf", symbol="symbol9664")]
   public class §false for while§ extends MovieClip
   {
      
      public var levelUp:MovieClip;
      
      public var hero_icon:MovieClip;
      
      private var §_-6X§:§class const for§;
      
      public function §false for while§(param1:§class const for§)
      {
         super();
         addFrameScript(0,this.frame1);
         this.§_-6X§ = param1;
         this.addEventListener(MouseEvent.CLICK,this.§function for finally§,false,0,true);
         this.addEventListener(MouseEvent.ROLL_OVER,this.§_-25§,false,0,true);
         this.addEventListener(MouseEvent.ROLL_OUT,this.§static if§,false,0,true);
         this.addEventListener(MouseEvent.MOUSE_DOWN,this.§_-po§,false,0,true);
         this.addEventListener(MouseEvent.MOUSE_UP,this.§_-Ct§,false,0,true);
      }
      
      public function §function for finally§(param1:MouseEvent) : void
      {
         if(this.§_-6X§.§null const null§)
         {
            return;
         }
         this.§_-6X§.game.gameSounds.playGUIButtonCommon();
         this.§_-6X§.addMapBlock();
         if(this.§_-6X§.§finally const finally§ != null)
         {
            this.§_-6X§.§finally const finally§.visible = false;
         }
         if(this.§_-6X§.§_-1C§ != null)
         {
            this.§_-6X§.game.showedLevelUp = true;
            this.§_-6X§.§_-1C§.visible = false;
         }
         this.§_-6X§.addChild(new §if const function§(this.§_-6X§.game));
         this.§_-6X§.§null const null§ = true;
      }
      
      protected function §_-25§(param1:MouseEvent) : void
      {
         this.§_-6X§.game.gameSounds.§break const null§();
         this.buttonMode = true;
         this.mouseChildren = false;
         this.useHandCursor = true;
         this.gotoAndStop("over");
         this.hero_icon.gotoAndStop(this.§_-6X§.game.gameHeroData.selectedHero.name);
      }
      
      protected function §static if§(param1:MouseEvent) : void
      {
         this.useHandCursor = false;
         this.gotoAndStop("idle");
         this.hero_icon.gotoAndStop(this.§_-6X§.game.gameHeroData.selectedHero.name);
      }
      
      protected function §_-po§(param1:MouseEvent) : void
      {
         this.gotoAndStop("press");
         this.hero_icon.gotoAndStop(this.§_-6X§.game.gameHeroData.selectedHero.name);
      }
      
      protected function §_-Ct§(param1:MouseEvent) : void
      {
         this.gotoAndStop("idle");
         this.hero_icon.gotoAndStop(this.§_-6X§.game.gameHeroData.selectedHero.name);
      }
      
      internal function frame1() : *
      {
         stop();
      }
   }
}

