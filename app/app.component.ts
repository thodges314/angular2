import { Component } from '@angular/core';

@Component({
  selector: 'my-app',
  template: `
  <h1>Hello, {{name}}</h1>
  <p>Email: {{email}}</p>
  <p>Address: {{address}}
  `,
})
export class AppComponent  {
	name = 'Thomas',
	email = 'thodges@javascriptonline.org',
	address = {
		street: '2125 Benicia Ct',
		city: 'Davis',
		state: 'CA'
	}
}
