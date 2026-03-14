export namespace backend {
	
	export class InstallOptions {
	    path: string;
	    autoStart: boolean;
	
	    static createFrom(source: any = {}) {
	        return new InstallOptions(source);
	    }
	
	    constructor(source: any = {}) {
	        if ('string' === typeof source) source = JSON.parse(source);
	        this.path = source["path"];
	        this.autoStart = source["autoStart"];
	    }
	}

}

