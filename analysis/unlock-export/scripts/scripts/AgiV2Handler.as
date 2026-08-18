package
{
   import flash.display.*;
   import flash.events.*;
   import flash.net.*;
   import flash.system.*;
   import flash.utils.*;
   
   public class AgiV2Handler implements §for const break§
   {
      
      public static var agi:*;
      
      public var §var var§:String = §each const each§.SERVICE_ARMORGAMES;
      
      public function AgiV2Handler()
      {
         super();
      }
      
      public static function §implements for super§(param1:String) : void
      {
         var §_-Tl§:URLRequest = null;
         var §_-hD§:URLLoader = null;
         var §_-FA§:String = param1;
         try
         {
            §var const super§.log("price: " + §each const each§.heroPrices[§_-FA§] + " - for sku: " + §_-FA§ + "for id: " + agi.user.getUID());
            §_-Tl§ = new URLRequest("http://stats.ironhidegames.com/krstats/api/sale?heroSku=" + §_-FA§ + "&source=armorgames&price=" + §each const each§.heroPrices[§_-FA§] + "&username=" + agi.user.getUID());
            §_-hD§ = new URLLoader();
            §_-hD§.load(§_-Tl§);
         }
         catch(err:Error)
         {
            §var const super§.log("Error: ",err);
         }
      }
      
      public function loadSystem(param1:Stage = null) : void
      {
         var agiURL:String;
         var loader:Loader;
         var stage:Stage = param1;
         §each const each§.menuLinkLabel = "armorG";
         §each const each§.LINK_SITE = "http://www.armorgames.com/?ref=KRFRONTIERS";
         agiURL = "http://agi.armorgames.com/assets/agi/AGI2.swf";
         Security.allowDomain("agi.armorgames.com");
         loader = new Loader();
         loader.contentLoaderInfo.addEventListener(IOErrorEvent.IO_ERROR,function(param1:IOErrorEvent):void
         {
         });
         loader.contentLoaderInfo.addEventListener(Event.COMPLETE,function(param1:Event):void
         {
            var e:Event = param1;
            agi = e.currentTarget.content;
            agi.connect({
               "stage":stage,
               "apiKey":"4D8E6105-019F-4899-B1AC-A26B9BD399D9",
               "callback":function(param1:Object):void
               {
                  if(!param1.success)
                  {
                     trace(param1.error);
                  }
               }
            });
         });
         loader.load(new URLRequest(agiURL));
      }
      
      public function retrieveHeroesPurchased(param1:§if const function§ = null) : void
      {
         var heroSkuArray:Array = null;
         var selectedPortrait:§_-re§ = null;
         var heroRoom:§if const function§ = param1;
         heroSkuArray = [];
         selectedPortrait = null;
         if(heroRoom != null)
         {
            selectedPortrait = §_-re§(heroRoom.selectedPortrait);
         }
         agi.content.retrievePurchases({
            "sku":"",
            "callback":function(param1:Object):void
            {
               var _loc2_:* = undefined;
               if(param1.success)
               {
                  _loc2_ = 0;
                  while(_loc2_ < param1.purchases.length)
                  {
                     heroSkuArray.push(param1.purchases[_loc2_].sku);
                     _loc2_++;
                  }
                  §each const each§.purchasedHeroes = heroSkuArray.concat();
                  if(heroRoom != null && heroRoom.isActive && §_-re§(heroRoom.selectedPortrait) == selectedPortrait && !heroRoom.checkPremiumContent(selectedPortrait.hero.name))
                  {
                     selectedPortrait.Click();
                  }
               }
               else
               {
                  trace(param1.error);
               }
            }
         });
      }
      
      public function showSingleHeroStoreForSku(param1:String, param2:§if const function§) : void
      {
         var selectedPortrait:§_-re§ = null;
         var heroArray:* = undefined;
         var sku:String = param1;
         var heroRoom:§if const function§ = param2;
         §var const super§.log("Call to showstore");
         selectedPortrait = §_-re§(heroRoom.selectedPortrait);
         heroRoom.§_-HD§();
         heroArray = [];
         agi.content.showStore({
            "sku":sku,
            "callback":function(param1:Object):void
            {
               var _loc2_:* = undefined;
               if(param1.success)
               {
                  switch(param1.response)
                  {
                     case agi.content.RESPONSE_USER_CANCELLED:
                        §var const super§.log("RESPONSE_USER_CANCELLED");
                        break;
                     case agi.content.RESPONSE_PURCHASE_FAILED:
                        §var const super§.log("RESPONSE_PURCHASE_FAILED");
                        break;
                     case agi.content.RESPONSE_PURCHASE_SUCCESS:
                        §var const super§.log("RESPONSE_PURCHASE_SUCCESS");
                        _loc2_ = 0;
                        while(_loc2_ < param1.purchases.length)
                        {
                           heroArray.push(param1.purchases[_loc2_].sku);
                           §var const super§.log("INSIDE DATA " + param1.purchases[_loc2_].sku + " - " + §each const each§.heroPrices[param1.purchases[_loc2_].sku]);
                           AgiV2Handler.§implements for super§(param1.purchases[_loc2_].sku);
                           _loc2_++;
                        }
                        §each const each§.purchasedHeroes = heroArray.concat(§each const each§.purchasedHeroes);
                        if(heroRoom.isActive && §_-re§(heroRoom.selectedPortrait) == selectedPortrait && !heroRoom.checkPremiumContent(selectedPortrait.hero.name))
                        {
                           §_-re§(heroRoom.selectedPortrait).Click();
                        }
                  }
                  heroRoom.onlinePurchaseWarning.markAsFinished();
               }
               else
               {
                  heroRoom.onlinePurchaseWarning.showError();
                  §var const super§.log("CallbackAgiError");
               }
               §var const super§.log("CallbackAgi");
            }
         });
      }
      
      public function callQuest(param1:String, param2:* = 1) : void
      {
         var key:String = param1;
         var value:* = param2;
         if(agi.user.isGuest())
         {
            return;
         }
         agi.quests.submit({
            "key":key,
            "progress":1,
            "callback":function(param1:Object):void
            {
               if(param1.success)
               {
                  trace("Users Current Progress:",param1.quest.progress);
                  trace("User Has Earned:",param1.quest.status.toLowerCase() == "completed");
               }
               else
               {
                  trace(param1.error);
               }
            }
         });
      }
      
      public function retrieveAllProductPrices() : void
      {
         var ret:Dictionary = null;
         ret = new Dictionary();
         agi.content.retrieveProducts({"callback":function(param1:Object):void
         {
            var _loc2_:* = undefined;
            if(param1.success)
            {
               _loc2_ = 0;
               while(_loc2_ < param1.products.length)
               {
                  ret[param1.products[_loc2_].sku] = param1.products[_loc2_].price;
                  _loc2_++;
               }
               §each const each§.heroPrices = ret;
            }
            else
            {
               trace(param1.error);
            }
         }});
      }
      
      public function isLoggedIn() : Boolean
      {
         return !agi.user.isGuest();
      }
      
      public function getAvatarUrl() : *
      {
         return AgiV2Handler.agi.user.getAvatarURL();
      }
      
      public function getUserName() : String
      {
         return AgiV2Handler.agi.user.getUsername();
      }
      
      public function retrieveOnlineData(param1:*) : void
      {
         AgiV2Handler.agi.storage.user.retrieve({
            "key":"",
            "callback":param1
         });
      }
      
      public function submitSave(param1:*, param2:*, param3:*) : void
      {
         AgiV2Handler.agi.storage.user.submit({
            "key":param1,
            "value":param2,
            "callback":param3
         });
      }
      
      public function deleteSave(param1:*, param2:*) : void
      {
         AgiV2Handler.agi.storage.user.erase({
            "key":param1,
            "callback":param2
         });
      }
      
      public function getService() : String
      {
         return this.§var var§;
      }
      
      public function openLogin() : void
      {
      }
   }
}

