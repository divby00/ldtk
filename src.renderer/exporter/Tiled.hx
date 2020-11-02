package exporter;

import led.Json;

class Tiled extends Exporter {
	static var TILED_VERSION = "1.4.2";
	static var MAP_VERSION = "1.4";

	public function new() {
		super();
	}

	override function convert() {
		super.convert();

		setOutputPath( projectPath.directory + "/" + projectPath.fileName+"_tiled", true );

		// Prepare world object
		var world = {
			maps: [],
			type: "world",
		};

		// Export each level to a separate TMX file
		var i = 1;
		var wx = 0;
		for(l in p.levels) {
			var bytes = exportLevel(l);

			var fp = outputPath.clone();
			fp.fileName = ( p.levels.length>1 ? '${i}_' : '' ) + l.identifier;
			fp.extension = "tmx";
			addOuputFile(fp.full, bytes);

			world.maps.push({
				fileName: fp.fileWithExt,
				x:wx,
				y:0,
			});
			wx += l.pxWid;
			i++;
		}

		// Create "world" JSON file
		log.fileOp("Creating world JSON...");
		var json = dn.JsonPretty.stringify(world);
		var fp = outputPath.clone();
		fp.fileName = projectPath.fileName;
		fp.extension = "world";
		addOuputFile(fp.full, haxe.io.Bytes.ofString(json));
	}


	function exportLevel(level:data.Level) : haxe.io.Bytes {
		log.add("level", "Converting level "+level.identifier+"...");

		var xml = Xml.createDocument();
		var layerId = 1;
		var objectId = 1;
		var gid = 1;


		/**
			Tiled a unique "grid size" value because it doesn't support different
			grid sizes in the same map file.
		**/
		var tiledGridSize = level.layerInstances.length==0 ? p.defaultGridSize : Const.INFINITE;
		for(li in level.layerInstances)
			tiledGridSize = M.imin(tiledGridSize, li.def.gridSize);
		var mapWidth = M.ceil( level.pxWid/tiledGridSize );
		var mapHeight = M.ceil( level.pxHei/tiledGridSize );

		/**
			MAP

			<map version="1.2" tiledversion="1.3.1" orientation="orthogonal" renderorder="right-down" compressionlevel="0" width="200" height="200" tilewidth="8" tileheight="8" infinite="0" backgroundcolor="#171c39" nextlayerid="35" nextobjectid="272">
		**/
		var map = Xml.createElement("map");
		xml.addChild(map);
		map.set("version", MAP_VERSION);
		map.set("tiledversion", TILED_VERSION);
		map.set("orientation", "orthogonal");
		map.set("renderorder", "right-down");
		map.set("compressionlevel", "0");
		map.set("width", ""+mapWidth);
		map.set("height", ""+mapHeight);
		map.set("tilewidth", ""+tiledGridSize);
		map.set("tileheight", ""+tiledGridSize);
		map.set("infinite", "0");
		map.set("backgroundcolor", C.intToHex(p.bgColor));

		/**
			TILESETS

			<tileset firstgid="1" name="cavesofgallet_tiles" tilewidth="8" tileheight="8" tilecount="384" columns="12">
				<image source="cavesofgallet_tiles.png" width="96" height="256"/>
			</tileset>
		**/
		var tilesetGids = new Map();
		for( td in p.defs.tilesets ) {
			log.add("tileset", 'Adding tileset ${td.identifier}...');
			if( td.padding!=0 )
				log.error('Tileset ${td.identifier} has padding, which isn\'t supported by Tiled which sucks bla fbklea lkez klz.');

			var count = M.ceil(td.pxWid/td.tileGridSize) * M.ceil(td.pxHei/td.tileGridSize);
			var tileset = Xml.createElement("tileset");
			map.addChild(tileset);
			tileset.set("firstgid",""+gid);
			tileset.set("name", td.identifier);
			tileset.set("tilewidth", ""+td.tileGridSize);
			tileset.set("tileheight", ""+td.tileGridSize);
			tileset.set("tilecount", "" + count);
			tileset.set("columns", "" + M.ceil(td.pxWid/td.tileGridSize) );
			tileset.set("objectalignment", "topleft" );
			tileset.set("margin", "0" );
			tileset.set("spacing", ""+td.spacing );

			var relPath = remapRelativePath(td.relPath);
			log.add("tileset", '  Adding image ${relPath}...');
			var image = Xml.createElement("image");
			tileset.addChild(image);
			image.set("source", relPath);
			image.set("width", ""+td.pxWid);
			image.set("height", ""+td.pxHei);

			tilesetGids.set(td.uid, gid);
			gid+=count;
		}

		function _remapTileId(tilesetUid:Int, tileId:Int, flips=0) : UInt {
			if( flips==0 )
				return tilesetGids.get(tilesetUid) + tileId;
			else {
				var gid : UInt = tilesetGids.get(tilesetUid) + tileId;
				log.debug("gid="+gid);

				if( M.hasBit(flips,0) ) {
					gid = M.setUnsignedBit(gid, 31);
					log.debug("flipX gid="+gid);
				}

				if( M.hasBit(flips,1) ) {
					gid = M.setUnsignedBit(gid, 30);
					log.debug("flipY gid="+gid);
				}

				return gid;
			}
		}


		/**
			LAYERS

			<layer id="32" name="collisions" width="200" height="200" opacity="0.79">
				<properties>
					<property name="advColl" type="bool" value="true"/>
				</properties>
				<data encoding="csv">...</data>
			</layer>
		**/
		function _createLayer(type:String, li:data.inst.LayerInstance, nameSuffix="") {
			var layer = Xml.createElement(type);
			map.addChild(layer);
			layer.set("id", Std.string(layerId++));
			layer.set("name", li.def.identifier + nameSuffix);
			switch type {
				case "layer":
					layer.set("width",""+li.cWid);
					layer.set("height",""+li.cHei);
					layer.set("opacity",""+li.def.displayOpacity);

				case "objectgroup":
			}
			return layer;
		}

		function _createTileObject(tilesetDefUid:Int, tileId:Int, x:Int, y:Int, flips=0) : Xml {
			var o = Xml.createElement("object");
			o.set("id", Std.string(objectId++));
			o.set("gid", ""+_remapTileId(tilesetDefUid, tileId, flips));
			o.set("x", ""+x);
			o.set("y", ""+y);
			o.set("width", ""+p.defs.getTilesetDef(tilesetDefUid).tileGridSize);
			o.set("height", ""+p.defs.getTilesetDef(tilesetDefUid).tileGridSize);
			return o;
		}

		var allInst = level.layerInstances.copy();
		allInst.reverse();
		for(li in allInst) {
			var ld = p.defs.layers.filter( (ld)->ld.uid==li.layerDefUid )[0];
			log.add("layer", "Layer "+ld.identifier+"...");


			switch ld.type {
				case IntGrid:
					log.warning("  Unsupported layer type "+ld.type);
					// if( ld.autoTilesetDefUid==null && ld.gridSize!=tiledGridSize ) {
					// 	log.error("IntGrid layer "+ld.identifier+" was not exported because it has a different gridSize (not supported by Tiled).");
					// 	continue;
					// }

					// IntGrid values
					// log.add("layer", "  Exporting IntGrid values...");
					// var layer = _createLayer("layer", li, "_values");
					// var data = Xml.createElement("data");
					// layer.addChild(data);
					// data.set("encoding","csv");
					// var csv = new Csv(li.cWid, li.cHei);
					// for(cy in 0...li.cHei)
					// for(cx in 0...li.cWid)
					// 	if( li.hasIntGrid(cx,cy) )
					// 		csv.set(cx,cy, li.getIntGrid(cx,cy)+1);
					// data.addChild( Xml.createPCData(csv.getString()) );

				case Entities:
					function _createProperty(props:Xml, name:String, type:Null<String>, val:Dynamic) {
						var prop = Xml.createElement("property");
						props.addChild(prop);
						prop.set("name", name);
						if( type!=null )
							prop.set("type", type);
						prop.set("value", Std.string(val));
						return prop;
					}

					var layer = _createLayer("objectgroup", li);
					for(e in li.entityInstances) {
						var object = Xml.createElement("object");
						layer.addChild(object);
						var x = e.x;
						var y = e.y;
						if( e.def.pivotX!=0 || e.def.pivotY!=0 ) {
							// log.warning('${e.def.identifier} entity uses a non-"topleft" pivot point which Tiled does not support.');
							x -= M.round(e.def.pivotX*e.def.width);
							y -= M.round(e.def.pivotY*e.def.height);
						}

						object.set("name",e.def.identifier);
						object.set("x",""+x);
						object.set("y",""+y);
						object.set("width",""+e.def.width);
						object.set("height",""+e.def.height);

						var props = Xml.createElement("properties");
						object.addChild(props);

						_createProperty(props, "__anchorX", "int", ""+e.x);
						_createProperty(props, "__anchorY", "int", ""+e.y);
						_createProperty(props, "__cx", "int", ""+e.getCx(ld));
						_createProperty(props, "__cy", "int", ""+e.getCy(ld));

						// Entity fields
						for(fi in e.fieldInstances)
						for( i in 0...fi.getArrayLength() ) {
							// Type
							var type = switch fi.def.type {
								case F_Int: "int";
								case F_Float: "float";
								case F_String: null;
								case F_Text: null;
								case F_Bool: "bool";
								case F_Color: "color";
								case F_Enum(enumDefUid): null;
								case F_Point: null;
							}
							// Value
							var v : Dynamic = switch fi.def.type {
								case F_Int: fi.getInt(i);
								case F_Float: fi.getFloat(i);
								case F_String, F_Text: fi.getString(i);
								case F_Bool: fi.getBool(i);
								case F_Color:
									var c = fi.getColorAsHexStr(i);
									c = c.substr(1);
									"#ff"+c;
								case F_Enum(enumDefUid): fi.getEnumValue(i);
								case F_Point: fi.getPointStr(i);
							}
							_createProperty(props, fi.def.identifier + (fi.getArrayLength()<=1 ? "" : "_"+i), type, v);
						}
					}

				case Tiles:
					// Detect stacked tiles
					var maxStack = 1;
					for( coordId in li.gridTiles.keys() )
						maxStack = M.imax(maxStack, li.gridTiles.get(coordId).length);
					log.debug(li.toString()+" => maxStack="+maxStack);

					// One Tiled-layer per "stack-layer"
					for( stackIdx in 0...maxStack ) {
						// Build CSV
						var layer = _createLayer("layer", li, maxStack>1 ? "_"+(stackIdx+1) : "");
						var csv = new Csv(li.cWid, li.cHei);
						for( coordId in li.gridTiles.keys() ) {
							var stack = li.gridTiles.get(coordId);
							if( stackIdx < stack.length ) {
								log.debug( stack[stackIdx].tileId+" f="+stack[stackIdx].flips );
								csv.setCoordId( coordId, _remapTileId(ld.tilesetDefUid, stack[stackIdx].tileId, stack[stackIdx].flips) );
							}
						}

						// Create layer XML
						var data = Xml.createElement("data");
						layer.addChild(data);
						data.set("encoding","csv");
						data.addChild( Xml.createPCData( csv.getString() ) );
					}


					// var layer = _createLayer("objectgroup", li);
					// for(coordId in li.gridTiles.keys()) {
					// 	for( tileInf in li.gridTiles.get(coordId) ) {
					// 		var o = _createTileObject(
					// 			ld.tilesetDefUid,
					// 			tileInf.tileId,
					// 			li.getCx(coordId)*ld.gridSize,
					// 			li.getCy(coordId)*ld.gridSize
					// 		);
					// 		layer.insertChild(o,0);
					// 	}
					// }


				case AutoLayer:
			}


			// Auto-layer tiles
			if( ld.autoTilesetDefUid!=null ) {
				log.add("layer", "  Exporting Auto-Layer tiles...");
				var td = p.defs.getTilesetDef(ld.autoTilesetDefUid);
				var layer = _createLayer("objectgroup", li, "_tiles");

				ld.iterateActiveRulesInDisplayOrder( (r)->{
					if( !li.autoTilesCache.exists(r.uid) )
						return;

					var ruleResults = li.autoTilesCache.get(r.uid);
					for(tiles in ruleResults)
					for( at in tiles ) {
						var o = _createTileObject(td.uid, at.tid, at.x, at.y, at.flips);
						layer.addChild(o);
					}
				});
			}
		}

		map.set("nextlayerid", ""+layerId);
		map.set("nextobjectid", ""+objectId);

		return haxe.io.Bytes.ofString( xml.toString() );
	}
}


private class Csv {
	var wid: Int;
	var hei: Int;
	var data: Map<Int, UInt>;

	public function new(w,h) {
		wid = w;
		hei = h;
		data = new Map();
	}

	public inline function set(cx,cy, v:UInt) {
		if( cx>=0 && cy>=0 )
			setCoordId(cx+cy*wid, v);
	}

	public inline function get(cx,cy) : UInt {
		return data.exists( cx+cy*wid ) ? data.get(cx+cy*wid) : 0;
	}

	public inline function getCoordId(coordId:Int) : UInt {
		return data.exists( coordId ) ? data.get( coordId ) : 0;
	}

	public inline function setCoordId(coordId:Int, v:UInt) {
		if( coordId<wid*hei )
			data.set(coordId, v);
	}

	public function getString() {
		var out : Array<String> = [];
		for(cy in 0...hei)
		for(cx in 0...wid)
			out.push( Std.string( get(cx,cy) ) );
		return out.join(",");
	}
}
