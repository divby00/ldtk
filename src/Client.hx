class Client extends dn.Process {
	public static var ME : Client;

	public var win(get,never) : nw.Window; inline function get_win() return nw.Window.get();
	public var jBody(get,never) : J; inline function get_jBody() return new J("body");
	// public var win(get,never) : js.html.Window; inline function get_win() return js.Browser.window;
	public var doc(get,never) : js.html.Document; inline function get_doc() return js.Browser.document;

	public function new() {
		super();

		ME = this;
		createRoot(Boot.ME.s2d);

		win.title = "LEd v"+Const.APP_VERSION;
		win.maximize();
		var e = new J('<div class="panel"/>');
		jBody.prepend(e);
		e.append( new J('<input type="text"/>') );
		e.append( new J('<input type="text"/>') );
		e.append( new J('<input type="text"/>') );

		var p = new data.ProjectData();
		p.createLevel();
		p.levels[0].layers[0].setIntGrid(0,0, 1);
		p.levels[0].layers[0].setIntGrid(2,4, 0);
		p.levels[0].layers[0].setIntGrid(5,5, 0);
		p.levels[0].layers[0].setIntGrid(6,6, 0);

		var lr = new render.LevelRender(p.levels[0]);
		lr.render();
	}

	override function onDispose() {
		super.onDispose();
		if( ME==this )
			ME = null;
	}
}
