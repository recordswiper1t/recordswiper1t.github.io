package
{
   import flash.geom.*;
   
   public class §dynamic else§ extends §extends const true§
   {
      
      internal var §_-ss§:Number;
      
      internal var previousPosition:Point;
      
      internal var speed:Number;
      
      internal var minRange:Number;
      
      internal var maxRange:Number;
      
      internal var damage:int;
      
      internal var destination:Point;
      
      internal var §get const function§:Number;
      
      internal var §extends static§:int;
      
      internal var §include native§:int;
      
      internal var callback:Function;
      
      internal var cRoot:Level;
      
      internal var §_-Wq§:Array;
      
      internal var §_-Qc§:§for const default§;
      
      private var §include each§:int;
      
      public function §dynamic else§(param1:Level, param2:Point, param3:Number, param4:Point, param5:Number, param6:int, param7:Object, param8:* = null)
      {
         super();
         this.previousPosition = new Point(0,0);
         this.§_-Qc§ = new §for const default§(new Point(0,0),param1);
         this.addChild(this.§_-Qc§);
         this.cRoot = param1;
         this.§_-ss§ = param3;
         this.x = param2.x;
         this.y = param2.y;
         this.§get const function§ = param5;
         this.destination = param4;
         this.speed = 13 * §_-Mm§.GAME_SCALE;
         this.§_-Wq§ = [this.destination.x - this.x,this.destination.y - this.y,this.§get const function§ - this.§_-ss§];
         if(this.vector3Length(this.§_-Wq§) > 0)
         {
            this.§_-Wq§[0] *= 1 / this.vector3Length(this.§_-Wq§);
            this.§_-Wq§[1] *= 1 / this.vector3Length(this.§_-Wq§);
            this.§_-Wq§[2] *= 1 / this.vector3Length(this.§_-Wq§);
         }
         this.§_-Wq§[0] *= this.speed;
         this.§_-Wq§[1] *= this.speed;
         this.§_-Wq§[2] *= this.speed;
         this.§extends static§ = 0;
         this.§include native§ = 0;
         this.minRange = param7.minRange;
         this.maxRange = param7.maxRange;
         this.damage = param6;
         var _loc9_:Point = §_-Mm§.ccpAdd(param2,§_-Mm§.ccp(0,param3));
         var _loc10_:Point = §_-Mm§.ccpAdd(param4,§_-Mm§.ccp(0,this.§get const function§));
         this.§_-Qc§.x = 0;
         this.§_-Qc§.y = this.§_-ss§;
         this.§_-Qc§.rotation = 57.29577951 * §_-Mm§.ccpToAngle(§_-Mm§.ccpSub(_loc10_,_loc9_));
         this.callback = param8;
         this.§include each§ = 1;
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
         param1.§_-qI§(new SoldierHeroDragonBurnEnemyModifier(this.cRoot,1,param1,_loc2_,_loc3_,_loc4_));
      }
      
      public function vector3Length(param1:Array) : Number
      {
         return Math.sqrt(param1[0] * param1[0] + param1[1] * param1[1] + param1[2] * param1[2]);
      }
      
      public function onFrameUpdate() : void
      {
         var _loc1_:EnemyCommon = null;
         --this.§include each§;
         if(this.§include each§ >= 0)
         {
            return;
         }
         this.previousPosition.x = this.x;
         this.previousPosition.y = this.y;
         if(this.travelToDestination(this.destination,this.speed))
         {
            if(this.§get const function§ < 0)
            {
               this.addExplosion2();
            }
            else
            {
               this.addExplosion1();
            }
            for each(_loc1_ in this.cRoot.enemies)
            {
               if(!_loc1_.isDead && _loc1_.isActive && !§_-Mm§.ellipseContains(this.x,this.y,_loc1_,this.minRange,this.cRoot.gameSettings.rangeRatio) && §_-Mm§.ellipseContains(this.x,this.y,_loc1_,this.maxRange,this.cRoot.gameSettings.rangeRatio))
               {
                  _loc1_.setDamage(this.damage,§_-Mm§.I_ARMOR);
                  if(this.cRoot.game.gameHeroData.heroAshbite.skill5.level > 0)
                  {
                     this.§_-Sj§(_loc1_);
                  }
               }
            }
            this.§_-hU§();
         }
         else
         {
            ++this.§include native§;
            if(this.§include native§ > this.§extends static§)
            {
               this.§_-fM§();
               this.§include native§ = 0;
            }
         }
      }
      
      public function addExplosion1() : void
      {
         var _loc1_:§extends const true§ = null;
         _loc1_ = new HeroDragonExplosion1(§_-Mm§.ccpAdd(§_-Mm§.ccpSub(new Point(this.x,this.y),§_-Mm§.wc2f(0,0)),§_-Mm§.ccp(0,this.§get const function§)),this.cRoot);
         this.cRoot.entities.addChild(_loc1_);
         this.cRoot.game.gameSounds.§_-2j§();
      }
      
      public function addExplosion2() : void
      {
         this.cRoot.entities.addChild(new §_-L2§(§_-Mm§.ccpAdd(§_-Mm§.ccpSub(new Point(this.x,this.y),§_-Mm§.wc2f(0,0)),§_-Mm§.ccp(0,this.§get const function§)),this.cRoot));
         this.cRoot.game.gameSounds.§_-2j§();
      }
      
      public function §_-fM§() : void
      {
         var _loc4_:Point = null;
         var _loc5_:HeroDragonParticle2 = null;
         var _loc1_:int = 2;
         var _loc2_:Point = §_-Mm§.ccpSub(new Point(this.x + 3,this.y - 6),this.previousPosition);
         var _loc3_:int = 0;
         while(_loc3_ < _loc1_)
         {
            _loc4_ = §_-Mm§.ccpMult(_loc2_,1 - Number(_loc3_) / Number(_loc1_));
            _loc5_ = new HeroDragonParticle2();
            _loc5_.§_-TW§(§_-Mm§.ccpAdd(§_-Mm§.ccpAdd(this.previousPosition,_loc4_),§_-Mm§.ccp(0,this.§_-ss§)),this.cRoot);
            _loc3_++;
         }
      }
      
      public function pause() : void
      {
         this.stop();
      }
      
      public function unPause() : void
      {
         this.play();
      }
      
      public function §_-hU§() : void
      {
         this.parent.removeChild(this);
      }
      
      public function travelToDestination(param1:Point, param2:Number) : Boolean
      {
         var _loc3_:Number = 1;
         var _loc4_:Point = §_-Mm§.ccpAdd(new Point(this.x,this.y),§_-Mm§.ccp(0,this.§_-ss§));
         var _loc5_:Number = this.§_-ss§ + this.§_-Wq§[2] * _loc3_;
         if(Math.abs(this.§get const function§ - this.§_-ss§) < Math.abs(_loc5_ - this.§_-ss§))
         {
            this.§_-ss§ = this.§get const function§;
         }
         else
         {
            this.§_-ss§ = _loc5_;
         }
         var _loc6_:Point = §_-Mm§.ccp(this.x + this.§_-Wq§[0],this.y + this.§_-Wq§[1]);
         if(§_-Mm§.ccpLength(§_-Mm§.ccpSub(param1,new Point(this.x,this.y))) < §_-Mm§.ccpLength(§_-Mm§.ccpSub(_loc6_,new Point(this.x,this.y))))
         {
            this.x = param1.x;
            this.y = param1.y;
         }
         else
         {
            this.x = _loc6_.x;
            this.y = _loc6_.y;
         }
         this.§_-Qc§.x = 0;
         this.§_-Qc§.y = this.§_-ss§;
         var _loc7_:Point = §_-Mm§.ccpAdd(new Point(this.x,this.y),§_-Mm§.ccp(0,this.§_-ss§));
         this.§_-Qc§.rotation = 57.29577951 * §_-Mm§.ccpToAngle(§_-Mm§.ccpSub(_loc7_,_loc4_));
         if(Math.abs(this.§get const function§ - this.§_-ss§) < param2)
         {
            return true;
         }
         return false;
      }
   }
}

