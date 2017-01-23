import { Component } from '@angular/core';

@Component({
  selector: 'user',
  template: `
  <h1>Hello, {{name}}</h1>
  <p><strong>Email:</strong> {{email}}</p>
  <p><strong>Address:</strong> {{address.street}} {{address.city}} {{address.state}}</p>
  `,
})
export class UserComponent  {
	name;
	email;
	address;

	constructor() {
		this.name = 'Thomas',
		this.email = 'thodges@javascriptonline.org',
		this.address = {
			street: '2125 Benicia Ct',
			city: 'Davis',
			state: 'CA'
		}

	}
}
